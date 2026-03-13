import inspect

import factory
from factory.alchemy import (
    SESSION_PERSISTENCE_COMMIT,
    SESSION_PERSISTENCE_FLUSH,
)
from factory.builder import BuildStep, StepBuilder, parse_declarations


class AsyncSQLAlchemyFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Asynchronous factory for SQLAlchemy
    supporting both 'create' and 'build' strategies.
    """

    @classmethod
    async def _generate(cls, strategy, params, session=None):
        if cls._meta.abstract:
            raise factory.errors.FactoryError(
                'Cannot generate instances of abstract factory %(f)s; '
                'Ensure %(f)s.Meta.model is set and %(f)s.Meta.abstract '
                'is either not set or False.' % dict(f=cls.__name__)
            )

        cls._meta.sqlalchemy_session = session
        cls._meta.sqlalchemy_session_persistence = 'flush'

        step = AsyncStepBuilder(cls._meta, params, strategy)
        return await step.build()

    @classmethod
    async def build(cls, **kwargs):
        return await cls._generate(factory.enums.BUILD_STRATEGY, kwargs)

    @classmethod
    async def create(cls, session, **kwargs):
        return await cls._generate(
            factory.enums.CREATE_STRATEGY, kwargs, session
        )

    @classmethod
    async def build_batch(cls, size, **kwargs):
        return [await cls.build(**kwargs) for _ in range(size)]

    @classmethod
    async def create_batch(cls, size, **kwargs):
        return [await cls.create(**kwargs) for _ in range(size)]

    @classmethod
    async def _build(cls, model_class, *args, **kwargs):
        for key, value in kwargs.items():
            if inspect.isawaitable(value):
                kwargs[key] = await value
        return model_class(*args, **kwargs)

    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        # First, build the object in memory, resolving any awaitable attributes
        instance = await cls._build(model_class, *args, **kwargs)

        # Then, persist it to the database.
        session = cls._meta.sqlalchemy_session
        if session is None:
            raise factory.errors.FactoryError(
                f'Cannot create {model_class.__name__} instance: '
                'sqlalchemy_session not set.'
            )

        await cls._save(session, instance)
        return instance

    @classmethod
    async def _save(cls, session, instance):
        session_persistence = cls._meta.sqlalchemy_session_persistence
        session.add(instance)
        if session_persistence == SESSION_PERSISTENCE_FLUSH:
            await session.flush()
        elif session_persistence == SESSION_PERSISTENCE_COMMIT:
            await session.commit()
        return instance


class AsyncStepBuilder(StepBuilder):
    """
    Orchestrates the generation process.
    Awaits the instantiation and post-generation hooks.
    """

    async def build(self, parent_step=None, force_sequence=None):
        pre, post = parse_declarations(
            self.extras,
            base_pre=self.factory_meta.pre_declarations,
            base_post=self.factory_meta.post_declarations,
        )

        if force_sequence is not None:
            sequence = force_sequence
        else:
            sequence = self.factory_meta.next_sequence()

        step = BuildStep(
            builder=self,
            sequence=sequence,
            parent_step=parent_step,
        )
        step.resolve(pre)

        args, kwargs = self.factory_meta.prepare_arguments(step.attributes)

        instance = await self.factory_meta.instantiate(
            step=step,
            args=args,
            kwargs=kwargs,
        )

        postgen_results = {}
        for declaration_name in post.sorted():
            declaration = post[declaration_name]
            declaration_result = declaration.declaration.evaluate_post(
                instance=instance,
                step=step,
                overrides=declaration.context,
            )
            if inspect.isawaitable(declaration_result):
                declaration_result = await declaration_result
            postgen_results[declaration_name] = declaration_result

        self.factory_meta.use_postgeneration_results(
            instance=instance,
            step=step,
            results=postgen_results,
        )
        return instance
