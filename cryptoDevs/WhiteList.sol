//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

// Address -> 0x552093aA618796baB3C7dc33b55ae69Cf0924913
contract Whitelist {

    uint8 public maxWhitelistedAddresses;

    mapping(address => bool) public isWhiteListed;
    
    uint8 public numAddressesWhitelisted;

    constructor(uint8 _maxWhitelistedAddresses) {
        maxWhitelistedAddresses =  _maxWhitelistedAddresses;
    }

    function addAddressToWhitelist() public {
        require(!isWhiteListed[msg.sender], "Sender has already been whitelisted");
        require(numAddressesWhitelisted < maxWhitelistedAddresses, "More addresses cant be added, limit reached");
        isWhiteListed[msg.sender] = true;
        numAddressesWhitelisted++;
    }
}