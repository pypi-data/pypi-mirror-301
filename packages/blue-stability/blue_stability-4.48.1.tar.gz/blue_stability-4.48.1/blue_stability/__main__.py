from blueness.argparse.generic import main

from blue_stability import NAME, VERSION, DESCRIPTION, ICON
from blue_stability.logger import logger


main(
    ICON=ICON,
    NAME=NAME,
    DESCRIPTION=DESCRIPTION,
    VERSION=VERSION,
    main_filename=__file__,
    logger=logger,
)
