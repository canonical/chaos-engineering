# Known limitations

Here we list the known limitations of the Canonical Chaos Engineering platform in its current state.

These are wide-scoped missing features (or products) that we would like to work on eventually.

For a list of known issues, bugs and feature requests that are currently being worked on or being tracked, refer to these issue trackers:

- https://github.com/canonical/chaos-engineering/issues
- https://github.com/canonical/litmus-operators/issues
- https://github.com/litmuschaos/litmus/issues


## Chaos testing for machine clouds
At the moment, the Canonical Chaos Engineering platform focuses on chaos-testing for k8s environments.
We are currently not looking into charmed VM cloud chaos testing; but that is definitely an interesting avenue for future development. Thoughts on the matter? Get in touch!

## TLS integration for the Litmus Control plane
Due to [an upstream bug](https://github.com/litmuschaos/litmus/issues/3136), at the moment the Litmus Control plane cannot talk over TLS to mongodb.
The `mongodb-k8s` charm's quite tolerant TLS integration approach means that even if MongoDB has a tls-certificates relation, it will not reject the Litmus components' traffic, but the traffic will nonetheless be unencrypted. So beware of this issue, and keep an eye on the upstream issue for when a fix will eventually be shipped.
