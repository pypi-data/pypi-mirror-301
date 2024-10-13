# dnsconfigurator
![GitLab Build Status](https://gitlab.com/ougar/dnsconfigurator/badges/main/pipeline.svg)


Python package I use to configure the DNS of my domain names. Keep a local DNS
configuration files - covering all my domains - up to date and use DNS
providers API to apply the configuration.

## How to use

Install the package. Look at the sample configuration. Fill out domain
information and select a DNS provider, get an API key, deploy the
configuration.

## Configuration
Check the sample config file using `dnsconfigurator sample` or `python -m dnsconfigurator
sample`

Create you own configuration file. Validate it with `dnsconfigurator -f configfile
validate` (default filename is `dns_config.yaml`

## Commands to use

 * ```list```
 * ```local```
 * ```remote```
 * ```compare```
 * ```status```
 * ```update```
 * ```dnscert```

## License

dnsconfigurator is distributed under the MIT license

## Contact

In the completely unexpected situation, that anyone else thinks this could be
useful, you are welcome to contact [Kristian
Hougaard](mailto:khougaard@gmail.com)

## ToDo

* Implement ```dnsconfigurator sample``` to show sample configuration.
* Better user documentation 
* Fix tests - they are ALL messed up
