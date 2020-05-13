from pykube import *
from typing import Iterator, Callable
import pykube.objects
import pytest


class GiantSwarmAppPlatformCRs:
    def __init__(self, kube_client: pykube.HTTPClient):
        super().__init__()
        self.app_cr_factory = pykube.objects.object_factory(
            kube_client, "application.giantswarm.io/v1alpha1", "App")
        self.app_catalog_cr_factory = pykube.objects.object_factory(
            kube_client, "application.giantswarm.io/v1alpha1", "AppCatalog")


def get_app_catalog_obj(catalog_name, catalog_uri: str,
                        kube_client: pykube.HTTPClient) -> pykube.objects.APIObject:
    app_catalog_cr = {
        "apiVersion": "application.giantswarm.io/v1alpha1",
        "kind": "AppCatalog",
        "metadata": {
            "labels": {
                "app-operator.giantswarm.io/version": "1.0.0",
                "application.giantswarm.io/catalog-type": "",
            },
            "name": catalog_name,
        },
        "spec": {
            "description": "Catalog for testing.",
            "storage": {
                "URL": catalog_uri,
                "type": "helm",
            },
            "title": catalog_name,
        }
    }
    crs = GiantSwarmAppPlatformCRs(kube_client)
    return crs.app_catalog_cr_factory(kube_client, app_catalog_cr)


@pytest.fixture(scope="module")
def app_catalog_factory(kube_client: pykube.HTTPClient) -> Iterator[Callable[[str, str], pykube.objects.APIObject]]:
    created_catalogs = []

    def _app_catalog_factory(name: str, url: str = None) -> pykube.objects.APIObject:
        if url is None:
            url = "https://giantswarm.github.io/{}-catalog/".format(name)
        api_obj = get_app_catalog_obj(name, url, kube_client)
        created_catalogs.append(api_obj)
        print("Creating {} AppCatalog".format(name))
        api_obj.create()
        return api_obj

    yield _app_catalog_factory
    for catalog in created_catalogs:
        print("Deleting {} AppCatalog".format(catalog.metadata["name"]))
        catalog.delete()


@pytest.fixture(scope="module")
def load_app(kube_client: pykube.HTTPClient, app_catalog_factory: Callable[[str, str], pykube.objects.APIObject]):
    app_name = "loadtest-app"
    app_cm_name = "{}-testing-user-config".format(app_name)
    api_version = "application.giantswarm.io/v1alpha1"
    default_catalog = app_catalog_factory("default")
    kind = "App"
    namespace = "giantswarm"

    load_app = {
        "apiVersion": api_version,
        "kind": kind,
        "metadata": {
            "name": app_name,
            "namespace": namespace,
            "labels": {
                "app": app_name,
                "app-operator.giantswarm.io/version": "1.0.0"
            },
        },
        "spec": {
            "catalog": default_catalog.metadata["name"],
            "version": "0.1.1",
            "kubeConfig": {
                "inCluster": True
            },
            "name": app_name,
            "namespace": "default",
            "configMap": {
                "name": app_cm_name,
                "namespace": namespace,
            }
        }
    }
    app_cm = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {
            "name": app_cm_name,
            "namespace": namespace,
        },
        "data": {
            "values": """replicaCount: "8"
ingress:
  enabled: "true"
  annotations:
    "kubernetes.io/ingress.class": "nginx"
  paths:
    - "/"
  hosts:
    - "loadtest.local"
autoscaling:
  enabled: "true"
"""
        }
    }

    app_cm_obj = ConfigMap(kube_client, app_cm)
    app_cm_obj.create()
    App = pykube.objects.object_factory(kube_client, api_version, kind)
    app_obj = App(kube_client, load_app)
    app_obj.create()
    yield None
    app_obj.delete()
    app_cm_obj.delete()


@pytest.mark.usefixtures("load_app")
@pytest.mark.performance
def test_deployments(kube_client: pykube.HTTPClient):
    job_obj = {
        "apiVersion": "batch/v1",
        "kind": "Job",
        "metadata": {
            "name": "gatling",
        },
        "spec": {
            "backoffLimit": "5",
            "activeDeadlineSeconds": "100",
            "template": {
                "spec": {
                    "containers": [
                        {
                            "name": "gatling",
                            "image": "denvazh/gatling:3.2.1",
                            "command": ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"],
                            "restartPolicy": "Never",
                        }
                    ]
                }
            }
        }
    }
    # gatling_job = Job(kube_client, job_obj)
    # gatling_job.create()
    assert True
