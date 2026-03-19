
    slope_classes = [
        {
            'code': 'flat',
            'min_slope': 0,
            'max_slope': 3,
            'translations': [
                {'locale': 'pt-BR', 'display_name': 'Plano', 'description': '0-3% declividade'},
                {'locale': 'en-US', 'display_name': 'Flat', 'description': '0-3% slope'},
                {'locale': 'es', 'display_name': 'Plano', 'description': '0-3% pendiente'},
            ]
        },
        {
            'code': 'gentle',
            'min_slope': 3,
            'max_slope': 8,
            'translations': [
                {'locale': 'pt-BR', 'display_name': 'Suave Ondulado', 'description': '3-8% declividade'},
                {'locale': 'en-US', 'display_name': 'Gently Sloping', 'description': '3-8% slope'},
                {'locale': 'es', 'display_name': 'Suavemente Ondulado', 'description': '3-8% pendiente'},
            ]
        },
        {
            'code': 'moderate',
            'min_slope': 8,
            'max_slope': 20,
            'translations': [
                {'locale': 'pt-BR', 'display_name': 'Ondulado', 'description': '8-20% declividade'},
                {'locale': 'en-US', 'display_name': 'Moderately Sloping', 'description': '8-20% slope'},
                {'locale': 'es', 'display_name': 'Ondulado', 'description': '8-20% pendiente'},
            ]
        },
        {
            'code': 'strong',
            'min_slope': 20,
            'max_slope': 45,
            'translations': [
                {'locale': 'pt-BR', 'display_name': 'Forte Ondulado', 'description': '20-45% declividade'},
                {'locale': 'en-US', 'display_name': 'Strongly Sloping', 'description': '20-45% slope'},
                {'locale': 'es', 'display_name': 'Fuertemente Ondulado', 'description': '20-45% pendiente'},
            ]
        },
        {
            'code': 'steep',
            'min_slope': 45,
            'max_slope': 100,
            'translations': [
                {'locale': 'pt-BR', 'display_name': 'Montanhoso', 'description': '>45% declividade'},
                {'locale': 'en-US', 'display_name': 'Steep', 'description': '>45% slope'},
                {'locale': 'es', 'display_name': 'Escarpado', 'description': '>45% pendiente'},
            ]
        },
    ]
