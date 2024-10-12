#  Copyright (c) 2022 Data Spree GmbH - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited.
#  Proprietary and confidential.

from typing import Dict


class AWSTask:

    def __init__(self, arn: str, details: Dict, lifetime: float) -> None:
        self.arn = arn
        self.details = details
        self.lifetime = lifetime
        self.update_time = 0
