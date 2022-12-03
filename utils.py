def get_geojson(features_list: list) -> str:
    """Збирає .geojson файл із записів, отриманий з бази даних.

    Мені простіше було написати так щоб не піздякатись зі схемою. Тим більше що все це вже у мене було
    на страшному Visual Basic. По суті, це навіть не  json, а скоріше повноцінний js, який лише зберігає
    інформацію і не виконує ніякої логіки. Такий собі уродець, народжений моїм незнанням JavaScript

    Args:
        features_list (list): ['тип_маркера', [('широта', 'довгота', 'назва', 'опис'),
                                'наступний_тип_маркера', [(,,,)],  ... ]

    Returns:
        str: var 'тип_маркера' = ... (і далі йде стандартна схема geojson, за тим винятком,
        що тут в один файл всунуті кілька змінних)
    """
    global_flag = False
    markers_geojson = 'var '
    for i in range(0, len(features_list), 2):
        if global_flag:             # Кома у кінці файлу. Пишемо її на початку, щоб не видаляти після останньої позиції
            markers_geojson += ''',
'''                                 # пропускаємо перед першим входженням
        else:
            global_flag = True
        markers_geojson += features_list[i] + ''' = {
    "type": "FeatureCollection",
    "features": ['''
        if features_list[i+1]:
            flag = False
            for feature in features_list[i+1]:
                if flag:                    # Кома, що розділяє словники з окремими позначками
                    markers_geojson += ''', ''' # пропускаємо перед першим входженням
                else:
                    flag = True
                markers_geojson += str(feature)
        markers_geojson += ''']
}'''
    return markers_geojson