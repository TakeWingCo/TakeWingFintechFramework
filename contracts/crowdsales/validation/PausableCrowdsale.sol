pragma solidity ^0.5.2;

import "../Crowdsale.sol";
import "./../../vendor/openzeppelin/contracts/lifecycle/Pausable.sol";

contract PausableCrowdsale is Crowdsale, Pausable
{
    function _preValidatePurchase(address token, uint value) internal view whenNotPaused {
        super._postValidatePurchase(token, value);
    }
}