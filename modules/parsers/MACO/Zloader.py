from cape_parsers.CAPE.core.Zloader import extract_config, rule_source
from maco.extractor import Extractor
from maco.model import ExtractorModel as MACOModel

from modules.parsers.utils import get_YARA_rule


def convert_to_MACO(raw_config: dict):
    if not (raw_config and isinstance(raw_config, dict)):
        return None

    parsed_result = MACOModel(family="Zloader", other=raw_config)

    if "Campaign ID" in raw_config:
        parsed_result.campaign_id = [raw_config["Campaign ID"]]

    if "RC4 key" in raw_config:
        parsed_result.encryption = [MACOModel.Encryption(algorithm="RC4", key=raw_config[:"RC4 key"])]

    for address in raw_config.get("address", []):
        parsed_result.http.append(MACOModel.Http(uri=address))

    return parsed_result


class Zloader(Extractor):
    author = "kevoreilly"
    family = "Zloader"
    last_modified = "2024-10-26"
    sharing = "TLP:CLEAR"
    yara_rule = get_YARA_rule(family)

    yara_rule = rule_source

    def run(self, stream, matches):
        return convert_to_MACO(extract_config(stream.read()))
