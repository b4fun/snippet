import dataclasses
import dns.resolver
import logging
import os
import psycopg2
import time


logger = logging.getLogger('flyio_kube_db')


@dataclasses.dataclass
class Config:
    """Config specifies the application configuration."""
    
    # DNS address for the flyio DNS
    flyio_dns: str
    # postgresql db host
    db_host: str
    # postgresql db port
    db_port: str
    # postgresql db user
    db_user: str
    # postgresql db password
    db_password: str

    @classmethod
    def init_from_env(cls):
        "Initializes configuration from environment variable."
        fields = dataclasses.fields(cls)
        values = {}
        for field in fields:
            field_env_name = field.name.upper()
            field_value = os.getenv(field_env_name)
            if field_value is None:
                if field.default is dataclasses.MISSING:
                    raise ValueError(f'{field_env_name} is required')
                continue
            values[field.name] = field_value
        return cls(**values)


def resolve_db_host(config: Config) -> str:
    """Resolves db host with fly DNS."""
    flyio_resolver = dns.resolver.Resolver()
    flyio_resolver.nameservers = [config.flyio_dns]
    answers = flyio_resolver.resolve(config.db_host, 'aaaa')
    for answer in answers:
        return answer.to_text()
    raise RuntimeError(f'no AAAA records resolved for {config.db_host}')


def connect_to_db(config: Config):
    """Open a connection to postgresql db."""
    logger.info(f'resolving db host from {config.db_host} DNS: {config.flyio_dns}')
    db_host_ip = resolve_db_host(config)
    logger.info(f'resolved db host ip: {db_host_ip}')

    return psycopg2.connect(
        # NOTE: for demo, we use database template1
        (f"dbname='template1' "
         f"user='{config.db_user}' "
         f"host='{db_host_ip}' "
         f"password='{config.db_password}'")
    )


def main():
    """Main entry of the demo."""
    config = Config.init_from_env()

    while True:
        logger.info('running query...')

        conn = connect_to_db(config)
        with conn.cursor() as cur:
            cur.execute("""SELECT datname from pg_database""")
            rows = cur.fetchall()
            for row in rows:
                print(f'fetched row: f{row[0]}')
        conn.close()

        time.sleep(5)


if __name__ == '__main__':
    main()