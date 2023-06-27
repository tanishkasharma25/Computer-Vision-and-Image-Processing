// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract GradCoin is ERC721, Ownable {
    struct StudentDetails {
        string name;
        uint256 cgpa;
        uint256 tokenBalance;
    }

    mapping(address => StudentDetails) public students;
    address[] private studentAddresses;
    uint256 public highestCGPA;
    address public BestStudent;
    address public professor;

    constructor() ERC721("GradCoin", "GC") {
        professor = msg.sender;
    }

//Modifier
    //Only Professor modifier
    modifier onlyProfessor() {
        require(msg.sender == professor, "Only the professor can perform this action");
        _;
    }


    //Only Professor can award tokens to students
    function GradCoinTransfer(string memory name, address studentAddress, uint8 cgpa) public onlyProfessor{
        require(cgpa >= 0 && cgpa <= 4, "CGPA must be between 0 and 4");
        uint256 tokens = 0;

        if (cgpa >= 3) {
            tokens = cgpa * 10 * 10**14; // 1 token = 0.0001 ETH
            }
        else if ((cgpa >= 2) && (cgpa < 3)) {
            tokens = cgpa * 7 * 10**14;
            }
        else if ((cgpa >= 1) && (cgpa < 2)) {
            tokens = cgpa * 5 * 10**14;
            }
        else {
            tokens = cgpa * 20 * 10**14;
            }

        // Check if the student already exists in the mapping
        if (students[studentAddress].cgpa > 0) {
            students[studentAddress].tokenBalance += tokens;
        } else {
        students[studentAddress] = StudentDetails(name, cgpa, tokens);
        studentAddresses.push(studentAddress);
        }

    if (cgpa > highestCGPA) {
        highestCGPA = cgpa;
        BestStudent = studentAddress;
    }
}

    function getStudentBalance(address studentAddress) public view returns (uint256 GradCoin) {
        uint256 totalBalance = 0;

        for (uint i = 0; i < studentAddresses.length; i++) {
            address addr = studentAddresses[i];
            if (addr == studentAddress) {
                totalBalance += students[addr].tokenBalance;
            }
        }

        return totalBalance;
    }


    function getHighestCGPA() public view onlyProfessor returns (uint256) {
        return highestCGPA;
    }

    function getBestStudent() public view onlyProfessor returns (string memory, uint256) {
        uint256 highestCGPA = 0;
        address bestStudentAddress;

        for (uint256 i = 0; i < studentAddresses.length; i++) {
            address studentAddress = studentAddresses[i];
            uint256 cgpa = students[studentAddress].cgpa;
            if (cgpa > highestCGPA) {
                highestCGPA = cgpa;
                bestStudentAddress = studentAddress;
                }
                }
        return (students[bestStudentAddress].name, highestCGPA);
    }

    function getAverageCGPA() public view returns (uint256) {
        uint256 sum = 0;
        for (uint i = 0; i < studentAddresses.length; i++) {
            sum += students[studentAddresses[i]].cgpa;
    }
        return sum / studentAddresses.length;
    }
}