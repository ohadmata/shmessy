import pandas as pd
from parametrization import Parametrization

from shmessy import Shmessy


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Regular data",
    df_data={
        "name": ["Guy", "Yaron", "Mish", "Moyiz"],
        "degree": ["MBA", "BCA", "M.Tech", "MBA"],
        "score": [90, 40, 80, 98]
    },
    fix_column_names=False,
    expected_result=["name", "degree", "score"]
)
@Parametrization.case(
    name="Fix space",
    df_data={
        "name space": ["Guy", "Yaron", "Mish", "Moyiz"],
        "degree": ["MBA", "BCA", "M.Tech", "MBA"],
        "score to 100": [90, 40, 80, 98]
    },
    fix_column_names=True,
    expected_result=["name_space", "degree", "score_to_100"]
)
@Parametrization.case(
    name="Fix special characters",
    df_data={
        "name&space": ["Guy", "Yaron", "Mish", "Moyiz"],
        "degree": ["MBA", "BCA", "M.Tech", "MBA"],
        "score%to@100": [90, 40, 80, 98]
    },
    fix_column_names=True,
    expected_result=["name_space", "degree", "score_to_100"]
)
@Parametrization.case(
    name="Fix special characters - FF turn off",
    df_data={
        "name&space": ["Guy", "Yaron", "Mish", "Moyiz"],
        "degree": ["MBA", "BCA", "M.Tech", "MBA"],
        "score%to@100": [90, 40, 80, 98]
    },
    fix_column_names=False,
    expected_result=["name&space", "degree", "score%to@100"]
)
def test_fix_column_names(df_data, fix_column_names, expected_result):
    shmessy = Shmessy(fix_column_names=fix_column_names)
    df = pd.DataFrame(df_data)
    df = shmessy.fix_schema(df=df)
    fixed_schema = shmessy.get_inferred_schema()
    assert [column for column in df] == expected_result
    assert [column.field_name for column in fixed_schema.columns] == expected_result


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Regular data",
    df_data={
        "name": ["Guy", "Yaron", "Mish", "Moyiz"],
        "degree": ["MBA", "BCA", "M.Tech", "MBA"],
        "score": [90, 40, 80, 98]
    },
    fix_column_names=False,
    expected_result=["name", "degree", "score"]
)
def test_issue_input_columns_as_object(df_data, fix_column_names, expected_result):
    df = pd.DataFrame(df_data).astype(object)
    df = Shmessy(fix_column_names=fix_column_names).fix_schema(df)
    assert [column for column in df] == expected_result

