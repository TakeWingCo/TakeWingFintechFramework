pragma solidity ^0.5.2;

import "../Crowdsale.sol";
import "./../validation/TimedCrowdsale.sol";

contract FinalizableCrowdsale is TimedCrowdsale
{
    event CrowdsaleFinalized();

    constructor() public
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