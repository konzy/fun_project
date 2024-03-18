from etl_munger import EtlMunger  # type: ignore


def main() -> None:
    em = EtlMunger(config_path='simple_config.yaml')
    result, errors = em.validate_and_transform('simple_csv.csv')
    print(result)
    print(errors)

    em.parse_and_write_files('simple_csv.csv',
                             'out/output.csv',
                             'out/failed.csv')



if __name__ == '__main__':
    main()
