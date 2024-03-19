from fun_project.etl_munger import EtlMunger  # type: ignore


def main() -> None:
    em = EtlMunger(config_path='simple_config.yaml')
    result, errors = em.validate_and_transform('simple_csv.csv')
    print(result)
    print(errors)


if __name__ == '__main__':
    main()
