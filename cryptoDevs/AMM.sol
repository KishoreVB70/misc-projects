// SPDX-License-Identifier: MIT 
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract AMM is ERC20{
    ERC20 token;
    address public tokenAddress;
    uint liquidity;
    uint tokenReserve;

    constructor(address _token) ERC20("Lp token", "LP"){
        tokenAddress = _token;
        token = ERC20(tokenAddress);
    }                                                                             

    // Here the function of liquidity is simply the eth contributed f(x,y) = y
    function addLiquidity(uint _amount) external payable returns(uint){
        require(msg.value > 0, "must send ether");
        require(_amount > 0, "should provide amount");

        uint _liquidity;
        uint totalEth = address(this).balance;
        uint ethBalance = totalEth - msg.value;

        uint tokenBalance = token.balanceOf(address(this));
        uint lpBalance = totalSupply();

        if(tokenBalance == 0){
            token.transferFrom(msg.sender,address(this), _amount);
            _liquidity = msg.value;
            _mint(msg.sender, _liquidity);
        }else{
            uint tokenAmount;
            //dy = dx*y / x
            tokenAmount = (msg.value * tokenBalance) / ethBalance;

            token.transferFrom(msg.sender, address(this), tokenAmount);

            //ds = dx*s/x
            _liquidity = (msg.value * lpBalance) / ethBalance;
            _mint(msg.sender, _liquidity);
        }
        return _liquidity;
    }

    // Based on the amount of LP tokens the user is willing to burn, he'll get the token and ether
    function removeLiquidity(uint lpAmount) external returns(uint _token, uint _ether){
        uint ethBalance = address(this).balance;
        uint tokenBalance = token.balanceOf(address(this));
        uint lpBalance = totalSupply();
        uint etherAmount;
        uint tokenAmount;
        //dx = ds * x/s 
        etherAmount = (lpAmount ) / (ethBalance * lpBalance);

        //dy = ds * y/ s 
        tokenAmount = (lpAmount) / (tokenBalance * lpBalance);

        payable(msg.sender).transfer(etherAmount);
        token.transferFrom(address(this), msg.sender, tokenAmount);

        _burn(msg.sender,lpAmount); 

        return(tokenAmount, etherAmount);
    }

    function etherToToken() external payable returns(uint _tokenAmount){
        require(msg.value > 0, "must send some ether");
        uint totalEth = address(this).balance;
        uint ethBalance = totalEth - msg.value;

        uint tokenBalance = token.balanceOf(address(this));

        uint amountToGive = calculateDY(msg.value, ethBalance, tokenBalance);
        token.transferFrom(address(this), msg.sender, amountToGive );

        return(amountToGive);
    }

    function tokenToEther(uint _token) external returns(uint _tokenAmount){
        require(_token > 0, "must send some token");

        uint ethBalance = address(this).balance;

        uint tokenBalance = token.balanceOf(address(this));


        uint amountToGive = calculateDY(_token, tokenBalance, ethBalance);
        token.transferFrom(msg.sender, address(this), _token );

        payable(msg.sender).transfer(amountToGive);

        return amountToGive;
    }

    function calculateDY(uint dx, uint x, uint y ) internal pure returns(uint){
        uint dy;
        // deducting 1% fees from input -> dx = dx - 1% of dx
        // Simplify -> dx99/100
        // Substitute in dy equation

        dy = ((dx * 99) * y) / ( (dx *99) + (x * 100) );
        return dy;
    }
}
