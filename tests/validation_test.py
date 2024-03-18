import os

from etl_munger import EtlMunger  # type: ignore

cwd = os.getcwd()
if 'tests' not in cwd:
    cwd = f'{cwd}/tests'


def test_correct_config() -> None:
    em = EtlMunger(config_path=f'{cwd}/test_files/success_config.yaml')
    result, errors = em.validate_and_transform(f'{cwd}/test_files/test_csv.csv')
    assert len(result) == 4
    assert str(result) == str("[['OrderID', 'OrderDate', 'ProductId', 'ProductName', 'Quantity', 'Unit'], [1, "
                              "datetime.date(2018, 1, 1), '1', 'PRODUCT', Decimal('10'), 'kg'], [9, datetime.date("
                              "2018, 1, 1), '1', 'PRODUCT', Decimal('10'), 'kg'], [10, datetime.date(2018, 1, 1), "
                              "'1', 'PRODUCT', Decimal('10'), 'kg']]")
    assert str(errors) == str("[['2', '2018', '19', '01', '2', 'Product 2', '20', 'val3', 'val4'], ['3', '2018', "
                              "'01', '100', '3', 'Product 3', '30', 'val5', 'val6'], ['4', '2018', '01', '01', "
                              "'bad_value', 'Product 4', '40', 'val7', 'val8'], ['5', '2018', '01', '01', '5', '5', "
                              "'50', 'val9', 'val10'], ['bad_value', '2018', '01', '01', '6', 'Product 6', '60', "
                              "'val11', 'val12'], ['7', '2018', '01', '01', '7', 'Product 7', 'bad_value', 'val13', "
                              "'val14'], ['8', '2018', '01', '01', '7', 'Product with lowercase and spaces', '20', "
                              "'val13', 'val14'], ['11', '2018', '01', '01', '7', 'ProductWithLowercase', '20', "
                              "'val13', 'val14'], ['12', '2018', '01', '01', '7', 'PRODUCT_WITH_UNDERSCORES', '20', "
                              "'val13', 'val14']]")
