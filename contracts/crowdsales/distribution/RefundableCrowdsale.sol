pragma solidity ^0.5.2;

import "./FinalizableCrowdsale.sol";

contract RefundableCrowdsale is FinalizableCrowdsale
{
    constructor(uint _goal) public
    {
        require(_goal > 0);
        goal = _goal;

        isGetFundActive = false;
    }

    function refund(address token) public 
    {
        require(finalized);
        require(!goalReached());

        ERC20(token).transfer(msg.sender, invested[msg.sender][token]);
    }

    function getFunds(address token) public
    {
        require(isGetFundActive);

        uint balance = ERC20(token).balanceOf(address(this));
        ERC20(token).transfer(wallet, balance);
    }

    function _updatePurchasingState(address token, uint value) internal
    {
        invested[msg.sender][token] += value;
    }

    function goalReached() public view returns (bool)
    {
        return totalInvested >= goal;
    }

    function _forwardFunds(address token, uint value) internal
    {
    }

    function _finalization() internal
    {
        if (goalReached())
        {
            isGetFundActive = true;
        }
    }

    uint public goal;

    bool public isGetFundActive;

    mapping(address => mapping(address => uint)) public invested;
}