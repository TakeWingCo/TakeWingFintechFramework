pragma solidity ^0.5.2;

import "../Crowdsale.sol";
import "./../../vendor/openzeppelin/contracts/access/roles/WhitelistedRole.sol";

contract WhitelistCrowdsale is WhitelistedRole, Crowdsale
{
    function _preValidatePurchase(address token, uint value) internal view {
        super._postValidatePurchase(token, value);
        require(isWhitelisted(msg.sender));
    }
}