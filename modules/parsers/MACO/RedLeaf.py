from cape_parsers.CAPE.core.RedLeaf import extract_config, rule_source
from maco.extractor import Extractor
from maco.model import ExtractorModel as MACOModel

from modules.parsers.utils import get_YARA_rule


def convert_to_MACO(raw_config: dict):
    if not (raw_config and isinstance(raw_config, dict)):
        return None

    parsed_result = MACOModel(family="RedLeaf", other=raw_config)

    for address in raw_config.get("c2_address", []):
        parsed_result.http.append(MACOModel.Http(hostname=address, usage="c2"))

    if "missionid" in raw_config:
        parsed_result.campaign_id.append(raw_config["missionid"])

    if "mutex" in raw_config:
        parsed_result.mutex.append(raw_config["mutex"])

    if "key" in raw_config:
        parsed_result.other["key"] = raw_config["key"]

    return parsed_result


class RedLeaf(Extractor):
    author = "kevoreilly"
    family = "RedLeaf"
    last_modified = "2024-10-26"
    sharing = "TLP:CLEAR"
    yara_rule = get_YARA_rule(family)

    yara_rule = rule_source

    def run(self, stream, matches):
        return convert_to_MACO(extract_config(stream.read()))
