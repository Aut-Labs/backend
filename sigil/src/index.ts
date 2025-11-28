import { SigilOutput } from "./AutSIgilGenerator/Sigil.model";
import { generateAutIdDAOSigil } from "./AutSIgilGenerator/SigilGenerator";
/**
 * generateSigilFromAddress
 * Generates AUT DAO Expander sigil from an address.
 *
 * @name generateSigilFromAddress
 * @function
 * @param {string} address The address to be used as a seed for the sigil
 * @return {Promise<SigilOutput>} Output options.
 */
export const generateSigilFromAddress = async (address: string) => {
  return generateAutIdDAOSigil(address);
};
