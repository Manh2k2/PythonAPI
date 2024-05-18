USE [CarDatabase]
GO
/****** Object:  Table [dbo].[Cars]    Script Date: 05/17/2024 6:27:51 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Cars](
	[CarID] [int] IDENTITY(1,1) NOT NULL,
	[Brand] [nvarchar](50) NULL,
	[Model] [nvarchar](50) NULL,
	[Year] [datetime] NULL,
	[Price] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[CarID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET IDENTITY_INSERT [dbo].[Cars] ON 

INSERT [dbo].[Cars] ([CarID], [Brand], [Model], [Year], [Price]) VALUES (1, N'Vinfast', N'VF3', 2024, 315000000)
INSERT [dbo].[Cars] ([CarID], [Brand], [Model], [Year], [Price]) VALUES (2, N'Vinfast', N'VFe34', 2021, 700000000)
INSERT [dbo].[Cars] ([CarID], [Brand], [Model], [Year], [Price]) VALUES (3, N'Vinfast', N'VF5', 2023, 479000000)
INSERT [dbo].[Cars] ([CarID], [Brand], [Model], [Year], [Price]) VALUES (4, N'Vinfast', N'VF6', 2023, 776000000)
INSERT [dbo].[Cars] ([CarID], [Brand], [Model], [Year], [Price]) VALUES (5, N'Vinfast', N'VF7', 2023, 1200000000)
INSERT [dbo].[Cars] ([CarID], [Brand], [Model], [Year], [Price]) VALUES (6, N'Vinfast', N'VF8', 2023, 1300000000)
INSERT [dbo].[Cars] ([CarID], [Brand], [Model], [Year], [Price]) VALUES (7, N'Vinfast', N'VF9', 2023, 1700000000)
SET IDENTITY_INSERT [dbo].[Cars] OFF
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_Cars]
AS
BEGIN
    DECLARE @json nvarchar(max) = N'{"ok":1,"msg":"ok","data":[';

    SELECT @json += FORMATMESSAGE(N'{"id":"%d","sid":"%d","value":"%s","time":"%s"},',
                              [CarID], [Year],[Price] , CONVERT(nvarchar(50),  [Brand]), CONVERT(nvarchar(50), [Model]))
    FROM Cars;

    IF RIGHT(@json, 1) = ','
    BEGIN
        SET @json = LEFT(@json, LEN(@json) - 1);
    END

    SET @json = @json + ']}';

    SELECT @json AS json;
END
GO
USE [master]
GO
ALTER DATABASE [CarDatabase] SET  READ_WRITE 
GO
