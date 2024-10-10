def get_versions():
    return versions[0]["number"]


versions = [
    {
        "number": "0.0.7",
        "features": [
            "1. fit the yxutil",
            "2. add keep_raw_id option to vmo2bimbam",
        ],
    },
    {
        "number": "0.0.6",
        "features": [
            "1. debug",
        ],
    },
    {
        "number": "0.0.5",
        "features": [
            "1. remove QUAL, FILTER and INFO from vmo, because it is too big and not necessary to store them in vmo",
        ],
    },
    {
        "number": "0.0.4",
        "features": [
            "1. Add stores QUAL, FILTER and INFO to vmo",
        ],
    },
    {
        "number": "0.0.3",
        "features": [
            "1. add command line interface",
        ],
    },
    {
        "number": "0.0.2",
        "features": [
            "1. convert vmo to bimbam",
            "2. bug fix",
            "3. add readme",
        ],
    },
    {
        "number": "0.0.1",
        "features": [
            "1. init",
            "2. VMO builds are included in the initial release, and it is now possible to easily convert vcf files into vmo. with vmo you can easily perform matrix extraction, as well as filter the data according to MAF or Miss ratio.",
            "3. Identity by states (IBS) calculations within a controlled memory and time range",
        ],
    },
]