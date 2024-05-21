use CarDatabase
go
CREATE PROCEDURE AddCar
    @Brand NVARCHAR(50),
    @Model NVARCHAR(50),
    @Year DateTime,
    @Price FLOAT
AS
BEGIN
    INSERT INTO Cars (Brand, Model, Year, Price)
    VALUES (@Brand, @Model, @Year, @Price);
END;

CREATE PROCEDURE GetCar
    @CarID INT
AS
BEGIN
    SELECT CarID, Brand, Model, Year, Price
    FROM Cars
    WHERE CarID = @CarID;
END;

CREATE PROCEDURE UpdateCar
    @CarID INT,
    @Brand NVARCHAR(50),
    @Model NVARCHAR(50),
    @Year DateTime,
    @Price FLOAT
AS
BEGIN
    UPDATE Cars
    SET Brand = @Brand, Model = @Model, Year = @Year, Price = @Price
    WHERE CarID = @CarID;
END;
CREATE PROCEDURE DeleteCar
    @CarID INT
AS
BEGIN
    DELETE FROM Cars
    WHERE CarID = @CarID;
END;
