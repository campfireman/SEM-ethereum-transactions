/*
 * thanks to Mastering Ethereum: building smart contracts and DApps p.118
 */

const ethTx = require("ethereumjs-tx")["Transaction"];
const txData = {
  nonce: "0x0",
  gasPrice: "0x09184e72a000",
  gasLimit: "0x30000",
  to: "0xb0920c523d582040f2bcb1bd7fb1c7c1ecebdb34",
  value: "0xde0b6b3a7640000",
  data:
    "0xa26e11860000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000a45696e7a61686c756e6700000000000000000000000000000000000000000000",
  v: "0x1c", // chainID des Ethereum-Mainnets
  r: 0,
  s: 0,
};

tx = new ethTx(txData);
console.log("RLP-Encoded Tx: 0x" + tx.serialize().toString("hex"));
txHash = tx.hash(); // This step encodes into RLP and calculates the hash
console.log("Tx Hash: 0x" + txHash.toString("hex"));

// Transaktion signieren
const privKey = Buffer.from(
  "91c8360c4cb4b5fac45513a7213f31d4e4a7bfcb4630e9fbf074f42a203ac0b9",
  "hex"
);
tx.sign(privKey);
console.log("v: " + tx.v.toString("hex"));
console.log("r: " + tx.r.toString("hex"));
console.log("s: " + tx.s.toString("hex"));
serializedTx = tx.serialize();
rawTx = "Signed Raw Transaction: 0x" + serializedTx.toString("hex");
console.log(rawTx);
