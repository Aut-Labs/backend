export const supportedNetworks = [
    'eth-mainnet',
    'polygon-mainnet',
    'polygon-amoy',
]

export const supportFunction = (networkName: string): boolean => {
    return supportedNetworks.find(x => x == networkName.toLocaleLowerCase()) != undefined;
}