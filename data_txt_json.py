def data_txt_json(file_name):
    # загрузка необходимых библиотек
    import pandas as pd
    # открытие файла
    with open(f"{file_name}.txt", 'r') as data:
        # представление текста как массива данных
        dataset = [line for line in data.readlines()]
    # удаление знака переноса строки
    n = len(dataset)
    dataset_n = [dataset[i].replace('\n', '') for i in range(n)]
    # обрезка текста с начала массива данных
    ind = dataset_n.index('[Data]')
    dataset_n = dataset_n[ind+1:]
    # разбивка каждого элемента массива по знаку нового столбца
    n = len(dataset_n)
    dataset_t = [dataset_n[i].split('\t') for i in range(n)]
    # представление элемента массива как таблицы pandas
    dataset_df = pd.DataFrame(dataset_t[1:], columns=dataset_t[0])
    # обрезка таблицы до необходимых столбцов
    dataset_df = dataset_df[['SNP Name', 'Sample ID', 'Allele1 - AB', 'Allele2 - AB']]
    # создание единого столбца 'Allele - AB'
    dataset_df['Allele - AB'] = dataset_df[['Allele1 - AB', 'Allele2 - AB']].agg(''.join, axis=1)
    dataset_df = dataset_df.drop(['Allele1 - AB', 'Allele2 - AB'], axis=1)
    # создание таблицы с необходимыми индексами и столбцами
    pivot_dataset = pd.pivot_table(dataset_df,
                               values='Allele - AB',
                               index='Sample ID',
                               columns = 'SNP Name',
                               aggfunc = lambda x: ''.join(x))
    # представление таблицы в json-формате
    dataset_json = pivot_dataset.to_json(f'{file_name}.json')
    return dataset_json

data_txt_json('dataset') # необходимо ввести только имя файла без расширения