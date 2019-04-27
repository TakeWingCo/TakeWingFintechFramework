pragma solidity ^0.5.2;

import "../Crowdsale.sol";

contract CappedCrowdsale is Crowdsale
{
    constructor(uint _cap, address _baseToken, address _wallet, address[] memory _availableTokens, uint[] memory _tokenPrices) Crowdsale(_baseToken, _wallet, _availableTokens, _tokenPrices) public 
    {
        require(
            cap > 0,
            "Cap should be more than 0"
        );

        cap = _cap;
    }

    function capReached() public view returns (bool) 
    {
        return totalInvested >= cap;
    }

    function _postValidatePurchase(address token, uint value) internal view {
        super._postValidatePurchase(token, value);
        require(totalInvested <= cap);
    }

    uint public cap;
}