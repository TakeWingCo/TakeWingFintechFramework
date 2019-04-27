pragma solidity ^0.5.2;

import "../Crowdsale.sol";
import "./../../vendor/openzeppelin/contracts/access/roles/WhitelistedRole.sol";

contract WhitelistedCrowdsale is WhitelistedRole, Crowdsale
{
    constructor(address _baseToken, address _wallet, address[] memory _availableTokens, uint[] memory _tokenPrices) Crowdsale(_baseToken, _wallet, _availableTokens, _tokenPrices) public 
    {
    }

    function _preValidatePurchase(address token, uint value) internal view {
        super._postValidatePurchase(token, value);
        require(isWhitelisted(msg.sender));
    }
}