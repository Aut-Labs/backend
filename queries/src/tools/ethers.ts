// Import the the ethers shims (**BEFORE** ethers)
// import '@ethersproject/shims';

// Import the ethers library
// Import the ethers library
import { ethers, Wallet } from "ethers";
import { NetworkConfig } from "../models/config";
import axios from "axios";

async function getSigner(networkConfig: NetworkConfig): Promise<ethers.Signer> {
  try {
    const provider = new ethers.providers.JsonRpcProvider(networkConfig.rpcUrls[0]);

    // Wait for the provider to connect and detect the network
    await provider.ready;

    console.log("Connected to network:", (await provider.getNetwork())?.name);

    let signer: ethers.Signer;
    if (process.env.DEPLOYER_PRIVATE_KEY) {
      const wallet = new Wallet(process.env.DEPLOYER_PRIVATE_KEY, provider);
      signer = wallet;
    } else {
      const senderWalletMnemonic = Wallet.fromMnemonic(
        process.env.MNEMONIC as string
      );
      signer = senderWalletMnemonic.connect(provider);
    }

    return signer;
  } catch (error) {
    console.error("Failed to initialize signer:", error);
    throw error;
  }
}
function ipfsCIDToHttpUrl(url: string, isJson: boolean) {
  if (!url.includes("https://"))
    return `${process.env.IPFS_GATEWAY}/${url.replace("ipfs://", "")}`;
  else return url;
}

async function getJSONFromURI(uri: string) {
  const result = await axios.get(uri);
  return result.data;
}

export { getSigner, ethers, ipfsCIDToHttpUrl, getJSONFromURI };
