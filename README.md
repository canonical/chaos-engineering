# Canonical Chaos Engineering Platform

This repository contains documentation for the Canonical Chaos Engineering Platform.

The documentation in its official form is available at https://canonical-chaos-engineering.readthedocs-hosted.com/en/latest/.

## What is Chaos Engineering?

According to the definition from [Wikipedia], Chaos engineering is the discipline of experimenting on a system 
in order to build confidence in the system's capability to withstand turbulent conditions in production.<br>
It is achieved by the intentional and controlled causing of failures in the system to understand their impact 
and find potential failure points. By doing so, engineers can proactively prevent outages and other disruptions.

Canonical Chaos Engineering Platform is an opinionated set of tools facilitating environment for conducting, observing
and analyzing output of Chaos engineering tests. The solution leverages [Juju] and a set of [Charmed Operators] 
to provide the end user with a smooth and frictionless experience of deploying and managing the solution throughout 
its entire lifecycle. 

## Contributing

You see room for improvement and would like to contribute to this documentation? You're more than welcome to do so!

Before contributing please see [CONTRIBUTING.md](CONTRIBUTING.md).

## Reporting an issue

Noticed a problem with our documentation? Tell us about it by [opening a bug].

[Wikipedia]: https://en.wikipedia.org/wiki/Chaos_engineering
[Juju]: https://juju.is/
[Charmed Operators]: https://juju.is/why-juju
[opening a bug]: https://github.com/canonical/chaos-engineering/issues
