import unittest
from os.path import abspath, dirname, join
from urllib.error import HTTPError
from rdf_utils.caching import read_file_and_cache
from rdf_utils.uri import URL_SECORO_M
from rdflib import Dataset
from rdf_utils.resolver import install_resolver


CWD = abspath(dirname(__file__))
ROOT_DIR = dirname(CWD)
EXEC_RQ = join(ROOT_DIR, "queries", "scenario-execution.rq")
SPEC_MODEL_URLS = {
    f"{URL_SECORO_M}/acceptance-criteria/bdd/templates/pickplace.tmpl.json": "json-ld",
    f"{URL_SECORO_M}/acceptance-criteria/bdd/variations/pickplace-secorolab-isaac.var.json": "json-ld",
}
EXEC_MODEL_URLS = {
    f"{URL_SECORO_M}/acceptance-criteria/bdd/execution/pickplace-secorolab-ros.obs.json": "json-ld",
}

class QueriesTest(unittest.TestCase):
    def setUp(self):
        install_resolver()

    def test_scenario_execution_query(self):
        graph = Dataset()
        for url, fmt in {**SPEC_MODEL_URLS, **EXEC_MODEL_URLS}.items():
            try:
                graph.parse(url, format=fmt)
            except HTTPError as e:
                raise RuntimeError(f"HTTPError for URL '{url}': {e}")

        exec_rq_str = read_file_and_cache(EXEC_RQ)
        q_result = graph.query(exec_rq_str)
        assert (
            q_result.type == "CONSTRUCT" and q_result.graph is not None
        ), "ScenarioExecution query did not return a graph"
        assert len(q_result.graph) > 0, "ScenarioExecution query returns an empty graph"
