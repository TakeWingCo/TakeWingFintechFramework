pragma solidity ^0.5.2;

import "./../vendor/openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Crowdsale
{
    event Invested(address indexed investor, address indexed token, uint amount);

    constructor(address _baseToken, address _wallet, address[] memory _availableTokens, uint[] memory _tokenPrices) public
    {
        require(
            _availableTokens.length == _tokenPrices.length,
            "Tokens amount is not equal to prices amount"
        );

        baseToken = _baseToken;
        wallet = _wallet;
        totalInvested = 0; 
        availableTokens = _availableTokens;
        
        for (uint i = 0; i < availableTokens.length; i++)
        {
            isToken[availableTokens[i]] = true;
            tokenPricePerBaseToken[availableTokens[i]] = _tokenPrices[i];
        } 
    }

    function invest(uint value, address token) external returns (bool)
    {
        _preValidatePurchase(token, value);

        uint tokenAmountToCreate = _getTokenAmount(token, value);

        ERC20(token).transferFrom(msg.sender, address(this), value);
        totalInvested += tokenAmountToCreate;

        _processPurchase(tokenAmountToCreate);
        emit Invested(msg.sender, token, value); 

        _updatePurchasingState(token, value);

        _forwardFunds(token, value);
        _postValidatePurchase(token, value);

        return true;
    }

    function _preValidatePurchase(address token, uint value) internal view
    {
        require(
            isToken[token] == true,
            "Invalid token address"
        );

        require(
            ERC20(token).allowance(msg.sender, address(this)) >= value,
            "Not enought allowance to transact"
        );
    }

    function _postValidatePurchase(address token, uint value) internal view
    {
    }

    function _deliverTokens(uint value) internal
    {
        ERC20(baseToken).transfer(msg.sender, value);
    }

    function _processPurchase(uint value) internal
    {
        _deliverTokens(value);
    }

    function _updatePurchasingState(address token, uint value) internal
    {
        
    }

    function _getTokenAmount(address token, uint value) internal view returns (uint)
    {
        return value / tokenPricePerBaseToken[token];
    }

    function _forwardFunds(address token, uint value) internal 
    {
        ERC20(token).transfer(wallet, value);
    }


    address public baseToken;

    address public wallet;

    address[] public availableTokens; 
    
    uint public totalInvested;

    mapping(address => bool) public isToken;

    mapping(address => uint) public tokenPricePerBaseToken;
}

