pragma solidity ^0.5.2;

import "../Crowdsale.sol";
import "./../../vendor/openzeppelin/contracts/token/ERC20/ERC20Mintable.sol";

contract MintedCrowdsale is Crowdsale
{
    function _deliverTokens(uint value) internal
    {
        ERC20Mintable(baseToken).mint(msg.sender, value);
    }
}