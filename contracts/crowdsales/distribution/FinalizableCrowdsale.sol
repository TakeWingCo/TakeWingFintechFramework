pragma solidity ^0.5.2;

import "../Crowdsale.sol";
import "./../validation/TimedCrowdsale.sol";

contract FinalizableCrowdsale is TimedCrowdsale
{
    event CrowdsaleFinalized();

    constructor(uint _openingTime, uint _closingTime, address _baseToken, address _wallet, address[] memory _availableTokens, uint[] memory _tokenPrices) TimedCrowdsale(_openingTime, _closingTime, _baseToken, _wallet, _availableTokens, _tokenPrices) public 
    {
        finalized = false;
    }

    function finalize() public 
    {
        require(!finalized);
        require(hasClosed());

        finalized = true;

        _finalization();
        emit CrowdsaleFinalized();
    }

    function _finalization() internal
    {
    }

    bool public finalized;
}