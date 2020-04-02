/*
 * Thanks to https://www.npmjs.com/package/ethereum-block-by-date
 */

main();

/*
 * -d <iso-datestring> get the date of a single block
 * -r <iso-datestring/iso-datestring> first and last block of specified range
 *
 * Example: node get_blocks.js -d "2016-07-20T13:20:40Z" -r "2019-09-02T12:00:00Z/2019-09-30T12:00:00Z"
 */
async function main() {
  var argv = require("minimist")(process.argv.slice(2));
  if (typeof argv["d"] === "undefined" && typeof argv["r"] === "undefined") {
    throw Error("no args specified");
  }
  const Web3 = require("web3");

  const web3 = new Web3("http://localhost:8545");

  const EthDater = require("ethereum-block-by-date");
  const dater = new EthDater(
    web3 // Web3 object, required.
  );

  if (argv["d"]) {
    try {
      // Getting block by date:
      let block = await dater.getDate(
        argv["d"], // Date, required. Any valid moment.js value: string, milliseconds, Date() object, moment() object.
        true // Block after, optional. Search for the nearest block before or after the given date. By default true.
      );
      console.log("Block on " + argv["d"]);
      console.log(block);
    } catch (err) {
      console.log(err);
    }
  }
  /* Returns an object: {
    date: '2016-07-20T13:20:40Z', // searched date
    block: 1920000 // block number
} */
  if (argv["r"]) {
    let dates = argv["r"].split("/");
    let start = dates[0];
    let end = dates[1];

    try {
      // Getting block by period duration. For example: every first block of Monday's noons of October 2019.
      let blocks = await dater.getEvery(
        "minutes", // Period, required. Valid value: years, quarters, months, weeks, days, hours, minutes
        start, // Start date, required. Any valid moment.js value: string, milliseconds, Date() object, moment() object.
        end, // End date, required. Any valid moment.js value: string, milliseconds, Date() object, moment() object.
        1, // Duration, optional, integer. By default 1.
        true // Block after, optional. Search for the nearest block before or after the given date. By default true.
      );
      console.log(
        "First and last blocks in range " + start + " - " + end + ":"
      );
      console.log(blocks[0]);
      console.log(blocks[blocks.length - 1]);
    } catch (err) {
      console.log(err);
    }
    /* Returns an array of objects: [
    { date: '2019-09-02T12:00:00Z', block: 8470641 },
    { date: '2019-09-09T12:00:00Z', block: 8515536 },
    { date: '2019-09-16T12:00:00Z', block: 8560371 },
    { date: '2019-09-23T12:00:00Z', block: 8605314 },
    { date: '2019-09-30T12:00:00Z', block: 8649923 }
    ] */
  }

  let requests = dater.requests;
  console.log("total requests: " + requests);
  /* Returns a count of made requests */
}
