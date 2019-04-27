pragma solidity ^0.5.2;

import "../Crowdsale.sol";
import "./../../vendor/openzeppelin/contracts/lifecycle/Pausable.sol";

contract PausableCrowdsale is Crowdsale, Pausable
{
    constructor(address _baseToken, address _wallet, address[] memory _availableTokens, uint[] memory _tokenPrices) Crowdsale(_baseToken, _wallet, _availableTokens, _tokenPrices) public
    {
    }

    function _preValidatePurchase(address token, uint value) internal view whenNotPaused {
        super._postValidatePurchase(token, value);
    }
}