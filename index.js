import Web3 from "web3";
import 'bootstrap/dist/css/bootstrap.css';
import configuration from '../build/contracts/GradCoin.json';

const contract_address = configuration.networks['5777'].address;
const contract_abi = configuration.abi;

const web3 = new Web3(
    Web3.givenProvider || 'http://127.0.0.1:7545'
);


const contract = new web3.eth.Contract(contract_abi, contract_address);

let account;

const accountEl = document.getElementById('account');

const main = async() =>{
    const accounts = await web3.eth.requestAccounts();
    account = accounts[0];
    accountEl.innerText = account;
};

main();


// async function transferTokens() {
//     const address = document.getElementById("student-address").value;
//     const name = document.getElementById("student-name").value;
//     const cgpa = document.getElementById("student-cgpa").value;

//     // Call the GradCoinTransfer function
//     const accounts = await web3.eth.getAccounts();
//     await gradCoinContract.methods.GradCoinTransfer(name, address, cgpa).send({
//       from: accounts[0],
//       value: 0
//     });

//     alert("Tokens transferred successfully!");
//   }

const gasPriceWei = web3.utils.toWei('30','gwei');
const gasLimit = 1000000;

const transferButton = document.getElementById("transfer");
transferButton.addEventListener('click', async () => {
    const address = document.getElementById("student-address").value;
    const name = document.getElementById("student-name").value;
    const cgpa = document.getElementById("student-cgpa").value;
    try {
        // call the GradCoinTransfer function in the smart contract
        await transferTokens(address, name, cgpa);

        // display a success message
        console.log(`Successfully transferred GradCoin tokens to ${address}.`);
      } catch (error) {
        // display an error message
        console.error(`Failed to transfer GradCoin tokens: ${error}`);
      }
});

async function transferTokens(address, name, cgpa) {
    try {
        // call the GradCoinTransfer function in the smart contract
        await contract.methods.GradCoinTransfer(name, address, cgpa).send({ from: account, gas: gasLimit });
    } catch (error) {
        throw error;
    }
}


