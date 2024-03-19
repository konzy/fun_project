from fun_project.etl_munger import EtlMunger  # type: ignore


def main() -> None:
    em = EtlMunger(config_path='simple_config.yaml')
    em.parse_and_write_files('simple_csv.csv',
                             'out/output.csv',
                             'out/failed.csv')


if __name__ == '__main__':
    main()
