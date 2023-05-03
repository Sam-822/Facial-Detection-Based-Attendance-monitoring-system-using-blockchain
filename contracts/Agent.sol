// SPDX-License-Identifier:MIT
pragma solidity ^0.8.0;


contract CSVStorage {
    struct CSVData {
        uint id;
        string name;
        string time;
        string date;
    }
    
    CSVData[] private csvData;

   
        function storeCSV(uint _id, string memory _name, string memory _time, string memory _date) public {
        CSVData memory newCSVData = CSVData(_id, _name, _time,_date);
        csvData.push(newCSVData);
    }
    
    
    function getCSV(uint _index) public view returns (uint, string memory, string memory,string memory) {
        return (csvData[_index].id, csvData[_index].name, csvData[_index].time,csvData[_index].date);
    }
    
    function getCSVCount() public view returns (uint) {
        return csvData.length;
    }
}