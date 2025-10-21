# Known limitations

Here we list the known limitations of the chaos engineering platform in its current state.

These are wide-scoped missing features (or products) that we would like to work on eventually.

For a list of known issues, bugs and feature requests that are currently being worked on or being tracked, refer to these issue trackers:

- https://github.com/canonical/chaos-engineering/issues
- https://github.com/canonical/litmus-operators/issues
- https://github.com/litmuschaos/litmus/issues


## Chaos testing for machine clouds.
At the moment, the chaos engineering platform focuses on chaos-testing for k8s clouds.
We are currently not looking into charmed VM cloud chaos testing; but that is definitely an interesting avenue for future development. Thoughts on the matter? Get in touch!

## Charmed Litmus chaos execution plane.
At the moment, the `litmus-operators` project only wraps the Chaos Control plane. Charming the Execution plane is something we'll be looking into in the near future, so stay tuned!

## TLS integration for the Litmus control plane.
Due to [an upstream bug](https://github.com/litmuschaos/litmus/issues/3136), at the moment the Litmus Control plane cannot talk over TLS to mongodb.
The `mongodb-k8s` charm's quite tolerant TLS integration approach means that even if MongoDB has a tls-certificates relation, it will not reject the Litmus components' traffic, but the traffic will nonetheless be unencrypted. So beware of this issue, and keep an eye on the upstream issue for when a fix will eventually be shipped.

## Admin password syncing for the Litmus Control plane.
At the moment, Litmus doesn't wipe the MongoDB tables upon teardown, which means that if you change the admin password and forget it, the only way to 'reset' it is manually deleting the tables in MongoDB or redeploying the `mongodb-k8s` charm altogether.
So beware that even if you redeploy the control plane, the user settings will be persisted in the database.
We're likely going to use juju-backed secret storage to manage the user credentials in an upcoming release, as admin credential management is a key aspect of implementing the Litmus execution plane, which we're going to work on soon (hopefully, delivered in 2026 Q2).
