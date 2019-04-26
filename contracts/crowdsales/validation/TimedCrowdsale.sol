pragma solidity ^0.5.2;

import "../Crowdsale.sol";

contract TimedCrowdsale is Crowdsale
{
    event TimedCrowdsaleExtended(uint prevClosingTime, uint newClosingTime);

    constructor(uint _openingTime, uint _closingTime, address _baseToken, address _wallet, address[] memory _availableTokens, uint[] memory _tokenPrices) Crowdsale(_baseToken, _wallet, _availableTokens, _tokenPrices) public
    {
        require(
            openingTime >= block.timestamp,
            "Opening time should be more or equal than current time"
        );

        require(
            closingTime > openingTime,
            "Closing time should be more than opening time"
        );

        openingTime = _openingTime;
        closingTime = _closingTime;
    }

    function isOpen() public view returns (bool) 
    {
        return block.timestamp >= openingTime && block.timestamp <= closingTime;
    }

    function hasClosed() public view returns (bool) 
    {
        return block.timestamp > closingTime;
    }

    function _preValidatePurchase(address token, uint value) internal view {
        super._postValidatePurchase(token, value);
        require(isOpen());
    }

    function _extendTime(uint newClosingTime) internal {
        require(!hasClosed());
        require(newClosingTime > closingTime);

        emit TimedCrowdsaleExtended(closingTime, newClosingTime);
        closingTime = newClosingTime;
    }

    uint public openingTime;
    uint public closingTime;
}