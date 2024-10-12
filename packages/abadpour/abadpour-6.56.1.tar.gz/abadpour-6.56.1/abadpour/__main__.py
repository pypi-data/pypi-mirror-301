from blueness.argparse.generic import main

from abadpour import NAME, VERSION, DESCRIPTION, ICON
from abadpour.build import build
from abadpour.logger import logger

main(
    ICON=ICON,
    NAME=NAME,
    DESCRIPTION=DESCRIPTION,
    VERSION=VERSION,
    main_filename=__file__,
    tasks={
        "build": lambda _: build(),
    },
    logger=logger,
)
