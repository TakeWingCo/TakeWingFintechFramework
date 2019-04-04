pragma solidity ^0.5.2;

import "./../vendor/openzeppelin/contracts/token/ERC20/ERC20.sol";
import "./../vendor/openzeppelin/contracts/token/ERC20/ERC20Mintable.sol";

contract Crowdsale
{
    enum StateICO
    {
        Initiated,
        Finished
    }

    event Invest(address indexed investor, address indexed token, uint amount);
    event EndICO(bool result);
    event GetFunds(address recipient, address indexed token, uint amount);

    constructor(address _baseToken, uint _goalInvested, address _wallet, address[] memory _availableTokens, uint[] memory _tokenPrices) public
    {
        require(
            _availableTokens.length == _tokenPrices.length,
            "Tokens amount is not equal to prices amount"
        );

        baseToken = _baseToken;
        wallet = _wallet;
        goalInvested = _goalInvested;
        totalInvested = 0; 
        availableTokens = _availableTokens;
        
        for (uint i = 0; i < availableTokens.length; i++)
        {
            isToken[availableTokens[i]] = true;
            tokenPricePerBaseToken[availableTokens[i]] = _tokenPrices[i];
        } 

        state = StateICO.Initiated;
    }

    function invest(uint value, address token) external returns (bool)
    {
        if (state == StateICO.Finished)
            return false;

        require(
            isToken[token] == true,
            "Invalid token address"
        );

        require(
            ERC20(token).allowance(msg.sender, address(this)) >= value,
            "Not enought allowance to transact"
        );

        uint tokenAmountToMint = value / tokenPricePerBaseToken[token];
        uint valueToInvest = tokenAmountToMint * tokenPricePerBaseToken[token];
        uint remainingToInvest = goalInvested - totalInvested;


        if (tokenAmountToMint > remainingToInvest)
        {
            tokenAmountToMint = remainingToInvest;
            valueToInvest = remainingToInvest * tokenPricePerBaseToken[token];

            state = StateICO.Finished;
            emit EndICO(true);
        }

        ERC20(token).transferFrom(msg.sender, address(this), valueToInvest);
        emit Invest(msg.sender, token, valueToInvest); 

        ERC20Mintable(baseToken).mint(msg.sender, tokenAmountToMint);
        totalInvested += tokenAmountToMint;

        invested[msg.sender][token] += valueToInvest;

        if (state == StateICO.Finished)
        {
            ERC20Mintable(baseToken).renounceMinter();
        }

        return true;
    }

    function getFunds(address token) external returns (uint)
    {
        require(
            isToken[token] == true,
            "Invalid token address"
        );

        require(
            state == StateICO.Finished,
            "ICO hasn't been finished"
        );

        uint availableBalance = ERC20(token).balanceOf(address(this));
        
        ERC20(token).transfer(wallet, availableBalance);
        emit GetFunds(wallet, token, availableBalance);

        return availableBalance;
    }


    address public baseToken;

    address public wallet;

    address[] public availableTokens; 

    uint public goalInvested;
    
    uint public totalInvested;

    mapping(address => bool) public isToken;

    mapping(address => uint) public tokenPricePerBaseToken;

    mapping(address => mapping(address => uint)) public invested;

    StateICO public state;
}

