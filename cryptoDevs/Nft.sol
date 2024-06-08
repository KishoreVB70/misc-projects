// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

// White list Address -> 0x552093aA618796baB3C7dc33b55ae69Cf0924913
// NFT address -> 0x4Fa80724b0fE36e7A2287C5B1ac02e3e9a23863b

interface IWhitelist {
    function isWhiteListed(address) external view returns (bool);
}

contract CryptoDevs is ERC721Enumerable, Ownable {

    IWhitelist whitelist;
    
    string _baseTokenURI;

    uint256 public _price = 0.01 ether;

    uint256 public presaleTiming;

    uint256 public maxTokenIds = 20;

    uint256 public tokenIds;
    
    bool public isPaused;

    bool public isPresaleStarted;

    uint256 public presaleEndTime;

    modifier onlyWhenNotPaused {
        require(!isPaused, "Contract currently paused");
        _;
    }

    modifier isTokenAvailable{
        require(tokenIds < maxTokenIds, "Out of tokens");
        _;
    }

    modifier isValueCorrect{
        require(msg.value >= _price, "Ether sent is not correct");
        _;
    }

//  <------------------------------------------------------------------------------------------------------------------------------>

    constructor (string memory baseURI, address whitelistContract, uint256 _presaleTiming) ERC721("Crypto Devs", "CD") {
        _baseTokenURI = baseURI;
        whitelist = IWhitelist(whitelistContract);
        presaleTiming = _presaleTiming;
    }

    function startPresale() public onlyOwner {
        isPresaleStarted = true;
        presaleEndTime = block.timestamp + presaleTiming;
    }

    function presaleMint() public payable onlyWhenNotPaused isTokenAvailable isValueCorrect{
        require(isPresaleStarted && block.timestamp < presaleEndTime, "Presale is not running");
        require(whitelist.whitelistedAddresses(msg.sender), "You are not whitelisted");
        tokenIds += 1;
        _safeMint(msg.sender, tokenIds);
    }

    function mint() public payable onlyWhenNotPaused isTokenAvailable isValueCorrect{
        require(isPresaleStarted && block.timestamp >=  presaleEndTime, "Presale has not ended yet");
        tokenIds += 1;
        _safeMint(msg.sender, tokenIds);
    }

    function _baseURI() internal view virtual override returns (string memory) {
        return _baseTokenURI;
    }

    function setPaused(bool val) public onlyOwner {
        isPaused = val;
    }

    function isWhitelisted() public returns(bool){
        return isWhiteListed.whitelistedAddresses(msg.sender);
    }

    function withdraw() public onlyOwner  {
        address _owner = owner();
        uint256 amount = address(this).balance;
        (bool sent, ) =  _owner.call{value: amount}("");
        require(sent, "Failed to send Ether");
    }

    receive() external payable {}

    fallback() external payable {}
}