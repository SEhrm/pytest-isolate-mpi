import pytest
import pytest_isolate_mpi


@pytest.mark.mpi(ranks=3)
def test_sum(mpi_ranks):
    assert False
