import sys
import logging
import click
import tldextract
import importlib
import dnsconfigurator
from dnsconfigurator.logger import setup_logger
from dnsconfigurator.dns_config import DNSConfig

logger = logging.getLogger("dnsconfigurator")
verbose_option = False


@click.group()
@click.option("-f", "--file",    default="./dns_config.yaml", help="Path to the configuration file")           # noqa
@click.option("-c", "--color",   is_flag=True, default=False, help="Enable colorized logging")                 # noqa
@click.option("-v", "--verbose", is_flag=True, default=False, help="Enable verbose logging (loglevel DEBUG)")  # noqa
@click.option("-q", "--quiet",   is_flag=True, default=False, help="Run quietly (loglevel WARN)")              # noqa
@click.option("-d", "--dryrun",  is_flag=True, default=False, help="Dryrun - don't make any changes")          # noqa
@click.option("-o", "--stdout",  is_flag=True, default=False, help="Send log to stdout in stead of stderr")    # noqa
@click.pass_context
def cli(ctx, file, color, verbose, quiet, dryrun, stdout):
    global verbose_option
    """DNS Manager CLI Tool"""
    setup_logger(color=color, verbose=verbose, quiet=quiet, stdout=stdout)
    verbose_option = verbose
    if dryrun:
        logger.warning("Making dryrun. No changes made")
    ctx.obj = {"file": file, "verbose": verbose, "dryrun": dryrun}


@cli.command()
@click.pass_context
def sample(ctx):
    logger.info("Showing sample configuration file")
    try:
        sample_path = importlib.resources.files(dnsconfigurator).joinpath("examples/sample_config.yaml")
        with sample_path.open("r") as f:
            sample_config = f.read()
    except FileNotFoundError:
        logger.error("Unable to find sample config. Is the package correctly installed?")
        raise
    logger.info("Sample configuration read. Content is now printed")
    print(sample_config)


@cli.command()
@click.pass_context
def list(ctx):
    logger.info("Running list command to show config domains")
    config = DNSConfig(filename=ctx.obj["file"])
    domains = {}
    for x in config.domains:
        domains[x] = config.domain(x)
    print("Config file read. Available domains:")
    for domain in domains:
        print(f"  - {domain:20} ({domains[domain].provider})")


@cli.command()
@click.pass_context
def status(ctx):
    logger.info("Running status command to show config domains")
    config = DNSConfig(filename=ctx.obj["file"])
    domains = {}
    for x in config.domains:
        domains[x] = config.domain(x)
    print("Domain status:")
    for name in domains:
        domain = domains[name]
        domain.fetch()
        domain.compare()
        status = "OK" if domain.uptodate() else "Need update"
        print(f"  - {name:20} ({domain.provider}) - {status}")


@cli.command()
@click.pass_context
@click.argument("fulldomain")
def provider(ctx, fulldomain):
    logger.info(f"Finding provider for domain {fulldomain}")
    config = DNSConfig(filename=ctx.obj["file"])
    dom = tldextract.extract(fulldomain)
    domain_name = f"{dom.domain}.{dom.suffix}"
    domain = config.domain(domain_name)
    provider = domain.provider
    logger.info(f"Provider for {domain_name} is {provider}")
    print(provider)


@cli.command()
@click.pass_context
@click.argument("domain")
def local(ctx, domain):
    logger.info(f"Showing local configuration of domain '{domain}'")
    config = DNSConfig(filename=ctx.obj["file"])
    domain = config.domain(domain)
    print(domain.show("records"))


@cli.command()
@click.pass_context
@click.argument("domain")
def remote(ctx, domain):
    logger.info(f"Showing remote configuration of domain '{domain}'")
    config = DNSConfig(filename=ctx.obj["file"])
    domain = config.domain(domain)
    domain.fetch()
    print(domain.show("remotes"))


@cli.command()
@click.pass_context
@click.argument("domain")
def compare(ctx, domain):
    logger.info("Running compare command")
    config = DNSConfig(filename=ctx.obj["file"])
    domain = config.domain(domain)
    domain.fetch()
    (add, delete, update) = domain.compare()
    print("Records to add")
    print("=================")
    for x in add:
        print(f" - {x}")
    print("")
    print("Records to delete")
    print("=================")
    for x in delete:
        print(f" - {x}")
    print("")
    print("Records to update")
    print("=================")
    for x in update:
        print(f" - From {x[1]}")
        print(f"   To   {x[0]}")
    # code.interact(local = locals())


@cli.command()
@click.pass_context
@click.argument("domain")
def update(ctx, domain):
    logger.info("Running update command")
    config = DNSConfig(filename=ctx.obj["file"])
    dryrun = ctx.obj["dryrun"]
    domain = config.domain(domain)
    domain.fetch()
    domain.compare()
    domain.sync(dryrun)


@cli.command()
@click.pass_context
@click.argument("certdomain")
@click.argument("challenge")
def dnscert(ctx, certdomain, challenge):
    logger.info("Running dnscert command")
    config = DNSConfig(filename=ctx.obj["file"])
    dryrun = ctx.obj["dryrun"]
    # Split domain into TLD and sub-domain-part
    # Create hostname part of acme challenge as _acme-challenge.subdomain
    value = "_acme-challenge"
    dom = tldextract.extract(certdomain)
    domain = f"{dom.domain}.{dom.suffix}"
    host = f"{value}.{dom.subdomain}" if dom.subdomain else value

    # Create domain object
    d = config.domain(domain)
    d.connect()
    if challenge == "remove":
        # Delete DNS challenge record
        logger.info(f"Removing DNS TXT record on {domain}")
        d.fetch()
        record_to_delete = None
        for record in d.remotes:
            if record.type == "TXT" and record.name == host:
                record_to_delete = record
                break
        if record_to_delete:
            logger.info(f"Found {value} TXT record and deleted it")
            if dryrun:
                logger.warning(f"Dryrun: Would have deleted record '{record.id}'")
            else:
                d.api.delete(record)
        else:
            logger.info(f"No {value} TXT record found")
    else:
        # Create DNS challenge record
        logger.info(f"Creating DNS TXT record on {domain}")
        record = d.add_txt(host, challenge)
        if dryrun:
            logger.warning(f"Dryrun: Would have created TXT record '{record.name}'")
        else:
            d.api.create(record)
        logger.info(f"TXT record '{record.name}' created")


def main():
    try:
        cli()
    except Exception as e:
        logger = logging.getLogger("dnsconfigurator")
        logger.error(f"{str(e)}")
        if verbose_option:
            # If verbose then raise again and print the whole stack trace
            raise
        else:
            # Otherwise just log that we failed and quit
            logger.error("Error caught. Quitting")
            sys.exit(1)


if __name__ == "__main__":
    main()
