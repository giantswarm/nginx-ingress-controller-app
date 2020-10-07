# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project's packages adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Remove unused prometheus annotations.

## [1.10.0] - 2020-10-07

### Changed

- Upgrade ingress-nginx-controller from v0.35.0 to [v0.40.2](https://github.com/kubernetes/ingress-nginx/blob/master/Changelog.md#0402).

  **Important** upstream changes to pay special attention to:

  - App/chart requires Kubernetes 1.16+ based platform release
    - It is recommended to change API group of Ingress resources from `extensions/v1beta1` to `networking.k8s.io/v1beta1` (available since Kubernetes 1.14)
  - Default configuration changes:
    - [`gzip-level`](https://github.com/kubernetes/ingress-nginx/blob/master/docs/user-guide/nginx-configuration/configmap.md#gzip-level) default changed from `5` to `1`
    - [`ssl-session-tickets`](https://github.com/kubernetes/ingress-nginx/blob/master/docs/user-guide/nginx-configuration/configmap.md#ssl-session-tickets) default changed from `true` to `false`
    - [`use-gzip`](https://github.com/kubernetes/ingress-nginx/blob/master/docs/user-guide/nginx-configuration/configmap.md#use-gzip) default changed from `true` to `false`
    - [`upstream-keepalive-connections`](https://github.com/kubernetes/ingress-nginx/blob/master/docs/user-guide/nginx-configuration/configmap.md#upstream-keepalive-connections) changed from `32` to `320`
    - [`upstream-keepalive-requests`](https://github.com/kubernetes/ingress-nginx/blob/master/docs/user-guide/nginx-configuration/configmap.md#upstream-keepalive-requests) changed from `100` to `10000`
- Support and enable by default [mimalloc](https://github.com/microsoft/mimalloc) as a drop-in malloc replacement to reduce nginx memory utilization.
- Support configuring additional environment variables for NGINX Ingress Controller container, to support configuring additional mimalloc [options](https://github.com/microsoft/mimalloc#environment-options).
- Adjust Helm `hook-delete-policy` and `hook-weight` to make admission webhook management more reliable.

## [1.9.2] - 2020-09-02

### Added

- `giantswarm.io/monitoring` label (in addition to existing annotation) for
  the new sharded TC Prometheus to pick up the service.

### Changed

- Upgrade to ingress-nginx [v0.35.0](https://github.com/kubernetes/ingress-nginx/blob/master/Changelog.md#0350).

## [1.9.1] - 2020-08-14

- Configure explicit helm hook weights to make validating webhook resource management reliable.

## [1.9.0] - 2020-08-13

- Support Ingress resources validating webhook.

## [1.8.4] - 2020-08-06

### Fixed

- Fix NetworkPolicy templating, to allow Pod ingress traffic (Prometheus scrape requests) on same port that the metrics/monitoring service advertises.

## [1.8.3] - 2020-07-31

### Fixed

- Fix controller RBAC permissions, granting "get" and "update" of leader election ConfigMap lock.

## [1.8.2] - 2020-07-31

### Fixed

- Fix controller RBAC permissions, granting "get" and "update" of leader election ConfigMap lock.

## [1.8.1] - 2020-07-28

### Added

- Make node ports configurable for NodePort Service type.

## [1.8.0] - 2020-07-24

### Breaking changes

In older releases the NGINX IC LoadBalancer Service name was hardcoded to `nginx-ingress-controller`. As of this release, to ensure the Service name uniqueness for multiple NGINX ICs per cluster support, the LoadBalancer Service name was made to be dynamic, derived from Helm release i.e. App Custom Resource (CR) name. Therefore, if you're upgrading from an older NGINX IC App release to v1.8.0+, existing NGINX IC LoadBalancer Service may get replaced by a new one for every NGINC IC App CR whose name is not `nginx-ingress-controller`.

When NGINX IC LoadBalancer Service gets recreated, cloud service provider (CSP) load balancer behind it gets recycled as well. It can take minute or so for ingress DNS records to be updated by `external-dns` and change propagated to clients. During that time there's ingress traffic downtime, since clients still resolve old no longer present CSP load balancer.

**Please take the potential ingress downtime (a minute or so) into consideration when planning the NGINX IC App upgrade from older to v1.8.0+.**

To make sure the downtime is shortest possible, external-dns availability is important precondition.
In recent platform releases (Azure v12.0.2, and AWS v12.1.4 and v11.5.4) we've improved external-dns monitoring and alerting.

**Therefore, before upgrading NGINX IC optional app to v1.8.0+, please make sure that your cluster has been upgraded to the latest platform release.**

### Added

- Support multiple NGINX IC App installations per tenant cluster.

### Removed

- Dropped support for deprecated configuration properties:
  - `configmap.annotations-prefix`
  - `configmap.default-ssl-certificate`
  - `configmap.hpa-enabled`
  - `configmap.hpa-max-replicas`
  - `configmap.hpa-min-replicas`
  - `configmap.hpa-target-cpu-utilization-percentage`
  - `configmap.hpa-target-memory-utilization-percentage`
  - `configmap.ingress-class`

## [1.7.3] - 2020-07-16

### Changed

- Upgrade to ingress-nginx [v0.34.1](https://github.com/kubernetes/ingress-nginx/blob/master/Changelog.md#0341).

## [1.7.2] 2020-07-10

### Changed

- Upgrade to ingress-nginx [v0.34.0](https://github.com/kubernetes/ingress-nginx/blob/master/Changelog.md#0340).

## [1.7.1] 2020-07-07

### Changed

- Support additional Service, for internal traffic. Existing Service can still be configured to be either for public (default) or internal traffic.
- Make monitoring headless Service non-optional.
- Enable managed app monitoring via monitoring service.

## [1.7.0] 2020-06-29

### Changed

- Use LoadBalancer Service on Azure.
- Change controller.service.type to LoadBalancer/NodePort, and introduce controller.service.public for public/internal service classification.
- Upgrade to ingress-nginx [0.33.0](https://github.com/kubernetes/ingress-nginx/blob/master/Changelog.md#0330).

## [1.6.12] 2020-06-04

### Changed

- Make healthcheck probes configurable.
- Make liveness probe more resilient.

## [1.6.11] 2020-05-26

### Changed

- Align labels, use `app.kubernetes.io/name` instead of `k8s-app` where possible.
  `k8s-app` remains to be used for compatibility reasons, as selectors are not modifiable without recreating the Deployment.

## [1.6.10] 2020-04-29

### Changed

- Make NGINX IC Service `externalTrafficPolicy` configurable and default to `Local`.

## [1.6.9] 2020-04-22

### Changed

- Restrict PodSecurityPolicy volumes to only those required (removes wildcard).
- Tune `net.ipv4.ip_local_port_range` to `1024 65535` as a safe sysctl.
- Tune `net.core.somaxconn` to `32768` via an initContainer with privilege escalation.
- Use `4` worker processes by default.
- Use upstream default of max-worker-connections of `16384`.
- Ignore NGINX IC Deployment replica count configuration when HorizontalPodAutoscaler is enabled.
- Drop unnecessary Helm release revision annotation from NGINX IC Deployment.
- Adjust README for display in the web interface context.

## [1.6.8] 2020-04-09

### Changed

- Default `max-worker-connections` to `0`, making it same as `max-worker-open-files` i.e. `max open files (system's limit) / worker-processes - 1024`.
  This optimizes for high load conditions where it improves performance at the cost of increasing RAM utilization (even on idle).
- HorizontalPodAutoscaler was tuned to use `targetMemoryUtilizationPercentage` of `80` due to increased RAM utilization with new default for `max-worker-connections` of `0`.
- Removed use of `enable-dynamic-certificates` CLI flag, it has been deprecated since [ingress-nginx 0.26.0](https://github.com/kubernetes/ingress-nginx/blob/master/Changelog.md#0260) via [ingress-nginx PR #4356](https://github.com/kubernetes/ingress-nginx/pull/4356)
- Changed default `error-log-level` from `error` to `notice`.
- Added a link to the README in the sources of Chart.yaml

## [1.6.7] 2020-04-08

### Changed

- Align graceful termination configuration with changes made in upstream ingress-nginx 0.26.0 (see [related PR #4487](https://github.com/kubernetes/ingress-nginx/pull/4487#issuecomment-525588554) and important section in [0.26.0 release notes](https://github.com/kubernetes/ingress-nginx/releases/tag/nginx-0.26.0)).
  - Make NGINX IC Deployment's `terminationGracePeriodSeconds` configurable and align its default with `configmap.worker-shutdown-timeout`
  - Make NGINX IC controller container lifecycle hooks configurable, and change from `sleep 60` to using `/wait-shutdown` as preStop hook.
- Make `controller.minReadySeconds` configurable.

## [1.6.6] 2020-04-01

### Changed

- Change deployment to use release revision not time for Helm 3 support.

## [1.6.5] 2020-03-23

### Changed

- Fix small cluster profile resource requests. ([#42](https://github.com/giantswarm/nginx-ingress-controller-app/pull/42))

## [1.6.4] 2020-03-17

### Changed

- Disable HPA and PDB for xs clusters since NGINX Deployment resource requests are not set there. ([#40](https://github.com/giantswarm/nginx-ingress-controller-app/pull/40))

## [1.6.3] 2020-03-16

### Changed

- Adjust resource requests, HPA and PDB depending on determined cluster profile; supported cluster profiles include xxs, xs, small, and larger than small or unknown. ([#38](https://github.com/giantswarm/nginx-ingress-controller-app/pull/38))

  By default, for nginx on:
  - xxs clusters - clear resource requests, HPA and PDB are disabled
  - xs clusters - clear resource requests, enabled HPA and PDB
  - small clusters - have some resource requests, HPA and PDB are enabled
  - clusters larger than small or unknown - have decent resource requests i.e. capacity out-of-the-box, and HPA and PDB are enabled.

## [1.6.2] 2020-03-12

### Changed

- Reintroduced config properties which should have been just deprecated but got dropped prematurely in v1.4.0 ([#36](https://github.com/giantswarm/nginx-ingress-controller-app/pull/36))
  - `configmap.annotations-prefix`
  - `configmap.default-ssl-certificate`
  - `configmap.hpa-enabled`
  - `configmap.hpa-max-replicas`
  - `configmap.hpa-min-replicas`
  - `configmap.hpa-target-cpu-utilization-percentage`
  - `configmap.hpa-target-memory-utilization-percentage`
  - `configmap.ingress-class`

## [1.6.1] 2020-03-10

### Changed

- Disable HPA, PDB and clear resource requests for extra small clusters. ([#34](https://github.com/giantswarm/nginx-ingress-controller-app/pull/34))

## [1.6.0] 2020-02-28

### Changed

- Upgrade to nginx-ingress-controller 0.30.0. ([#31](https://github.com/giantswarm/nginx-ingress-controller-app/pull/31))
- Configured app icon. ([#32](https://github.com/giantswarm/nginx-ingress-controller-app/pull/32))
- Enabled HorizontalPodAutoscaler by default. ([#27](https://github.com/giantswarm/nginx-ingress-controller-app/pull/27))
- Based on HPA trials done so far, following settings have been adjusted to better fit actual observed usage profiles:
  - CPU resource requests have been adjusted from 500m to 2 CPU
    - 0.5 CPU was not enough for all the processes NGINX Ingress Controller starts
  - Memory requests changed from 600Mi to 2.5GB
    - Scaling out does not shard Ingress definitions and other configurations stored in memory of every nginx-ingress-controller replica
    - Memory usage spikes during configuration reloads
    - It improves the HPA stability
  - Default number of nginx worker processes was changed from 4 to 1
    - This reduced memory usage of each replica
    - It didn't affect request handling capacity
    - Better defaults considering CPU requests and number of processes running on every nginx-ingress-controller replica.
- To avoid cluster-operator and HPA collision and nginx service disruption, this release also breaks with cluster-operator controllable nginx ingress controller Deployment replicas count
  - `ingressController.replicas` which was previously dynamically set by cluster-operator is now removed
  - New `controller.replicaCount` config property is introduced, default replica count is set to 1, and then by default enabled HPA takes it over from there, by default scaling the Deployment in range of 1 to 20 replicas
  - If HPA gets disabled on-demand, replica count will stay static if not manually or automatically changed by some third party.

## [1.5.0] 2020-02-18

### Changed

- Disable nginx NodePort Service by default, having legacy cluster-operator enable it for legacy Azure only. ([#29](https://github.com/giantswarm/nginx-ingress-controller-app/pull/29))
- Upgrade to nginx-ingress-controller 0.29.0. ([#30](https://github.com/giantswarm/nginx-ingress-controller-app/pull/30))

## [1.4.0] 2020-02-10

### Changed

- Support overriding all nginx configmap settings. ([#26](https://github.com/giantswarm/nginx-ingress-controller-app/pull/26))

## [1.3.0] 2020-01-30

### Changed

- Upgrade to nginx-ingress-controller 0.28.0. ([#24](https://github.com/giantswarm/nginx-ingress-controller-app/pull/24))

## [1.2.1] 2020-01-29

### Changed

- Support proxy protocol for AWS. ([#23](https://github.com/giantswarm/nginx-ingress-controller-app/pull/23))

## [1.2.0] 2020-01-21

### Changed

- Upgrade to nginx-ingress-controller 0.27.1. ([#20](https://github.com/giantswarm/nginx-ingress-controller-app/pull/20))
- Add metrics Service for prometheus-operator support. ([#19](https://github.com/giantswarm/nginx-ingress-controller-app/pull/19))
- Allow overriding of nginx SSL protocol default setting. ([#17](https://github.com/giantswarm/nginx-ingress-controller-app/pull/17))

## [1.1.1] 2020-01-04

### Changed

- Updated manifests for Kubernetes 1.16. ([#16](https://github.com/giantswarm/nginx-ingress-controller-app/pull/16))

## [1.1.0]

### Changed

- Migrate to managed application structure.

[kubernetes-nginx-ingress-controller](https://github.com/giantswarm/kubernetes-nginx-ingress-controller) repository is deprecated.

Previous versions changelog can be found [here](https://github.com/giantswarm/kubernetes-nginx-ingress-controller/blob/master/CHANGELOG.md)

[Unreleased]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.10.0...HEAD
[1.10.0]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.9.2...v1.10.0
[1.9.2]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.9.1...v1.9.2
[1.9.1]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.9.0...v1.9.1
[1.9.0]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.8.4...v1.9.0
[1.8.4]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.8.3...v1.8.4
[1.8.3]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.8.2...v1.8.3
[1.8.2]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.8.1...v1.8.2
[1.8.1]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.8.0...v1.8.1
[1.8.0]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.7.3...v1.8.0
[1.7.3]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.7.2...v1.7.3
[1.7.2]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.7.1...v1.7.2
[1.7.1]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.7.0...v1.7.1
[1.7.0]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.6.12...v1.7.0
[1.6.12]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.6.11...v1.6.12
[1.6.11]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.6.10...v1.6.11
[1.6.10]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.6.9...v1.6.10
[1.6.9]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.6.8...v1.6.9
[1.6.8]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.6.7...v1.6.8
[1.6.7]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.6.6...v1.6.7
[1.6.6]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.6.5...v1.6.6
[1.6.5]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.6.4...v1.6.5
[1.6.4]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.6.3...v1.6.4
[1.6.3]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.6.2...v1.6.3
[1.6.2]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.6.1...v1.6.2
[1.6.1]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.6.0...v1.6.1
[1.6.0]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.2.1...v1.3.0
[1.2.1]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/giantswarm/nginx-ingress-controller-app/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/giantswarm/nginx-ingress-controller-app/releases/tag/v1.1.0
