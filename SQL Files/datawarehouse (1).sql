-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le :  mer. 13 mai 2020 à 17:48
-- Version du serveur :  10.4.10-MariaDB
-- Version de PHP :  7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `datawarehouse`
--

-- --------------------------------------------------------

--
-- Structure de la table `dimconcept`
--

DROP TABLE IF EXISTS `dimconcept`;
CREATE TABLE IF NOT EXISTS `dimconcept` (
  `conceptID` int(11) NOT NULL AUTO_INCREMENT,
  `conceptLabel` varchar(30) NOT NULL,
  PRIMARY KEY (`conceptID`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `dimconcept`
--

INSERT INTO `dimconcept` (`conceptID`, `conceptLabel`) VALUES
(1, 'panicbuying'),
(2, 'stayathome');

-- --------------------------------------------------------

--
-- Structure de la table `dimlanguage`
--

DROP TABLE IF EXISTS `dimlanguage`;
CREATE TABLE IF NOT EXISTS `dimlanguage` (
  `languageID` int(11) NOT NULL AUTO_INCREMENT,
  `languageCode` varchar(4) NOT NULL,
  `languageName` varchar(30) NOT NULL,
  PRIMARY KEY (`languageID`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `dimlanguage`
--

INSERT INTO `dimlanguage` (`languageID`, `languageCode`, `languageName`) VALUES
(1, 'zh', 'Chinese'),
(2, 'en', 'English'),
(3, 'und', 'und'),
(4, 'de', 'German'),
(5, 'ja', 'Japanese'),
(6, 'es', 'Spanish');

-- --------------------------------------------------------

--
-- Structure de la table `dimlocation`
--

DROP TABLE IF EXISTS `dimlocation`;
CREATE TABLE IF NOT EXISTS `dimlocation` (
  `locationID` int(11) NOT NULL AUTO_INCREMENT,
  `locationAltID` varchar(30) NOT NULL,
  `cityName` varchar(30) NOT NULL,
  `countryID` varchar(2) NOT NULL,
  `countryName` varchar(30) NOT NULL,
  `continentID` varchar(2) NOT NULL,
  `continentName` varchar(13) NOT NULL,
  PRIMARY KEY (`locationID`)
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `dimlocation`
--

INSERT INTO `dimlocation` (`locationID`, `locationAltID`, `cityName`, `countryID`, `countryName`, `continentID`, `continentName`) VALUES
(1, 'ND', 'ND', 'ND', 'ND', 'ND', 'ND'),
(2, 'NDusa', 'ND', 'US', 'united states', 'NA', 'North America'),
(3, 'brightonGBR', 'brighton', 'GB', 'united kingdom', 'EU', 'Europe'),
(4, 'glasgowGBR', 'glasgow', 'GB', 'united kingdom', 'EU', 'Europe'),
(5, 'atlantaUSA', 'atlanta', 'US', 'united states', 'NA', 'North America'),
(6, 'NDGBR', 'ND', 'GB', 'united kingdom', 'EU', 'Europe'),
(7, 'bandungIDN', 'bandung', 'ID', 'indonesia', 'AS', 'Asia'),
(8, 'louisvilleUSA', 'louisville', 'US', 'united states', 'NA', 'North America'),
(9, 'NDIN', 'ND', 'in', 'india', 'AS', 'Asia'),
(10, 'caliCOL', 'cali', 'CO', 'colombia', 'SA', 'South America'),
(11, 'losangelesUSA', 'los angeles', 'US', 'united states', 'NA', 'North America'),
(12, 'NDIND', 'ND', 'IN', 'india', 'AS', 'Asia'),
(13, 'londonCAN', 'london', 'CA', 'canada', 'NA', 'North America'),
(14, 'NDCAN', 'ND', 'CA', 'canada', 'NA', 'North America'),
(15, 'parisFRA', 'paris', 'FR', 'france', 'EU', 'Europe'),
(16, 'berlinDEU', 'berlin', 'DE', 'germany', 'EU', 'Europe'),
(17, 'guadalajaraMEX', 'guadalajara', 'MX', 'mexico', 'NA', 'North America'),
(18, 'NDMYS', 'ND', 'MY', 'malaysia', 'AS', 'Asia');

-- --------------------------------------------------------

--
-- Structure de la table `dimsentiment`
--

DROP TABLE IF EXISTS `dimsentiment`;
CREATE TABLE IF NOT EXISTS `dimsentiment` (
  `sentimentID` int(11) NOT NULL AUTO_INCREMENT,
  `sentimentLabel` varchar(20) NOT NULL,
  PRIMARY KEY (`sentimentID`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `dimsentiment`
--

INSERT INTO `dimsentiment` (`sentimentID`, `sentimentLabel`) VALUES
(1, 'neutral'),
(2, 'positive'),
(3, 'negative');

-- --------------------------------------------------------

--
-- Structure de la table `dimsource`
--

DROP TABLE IF EXISTS `dimsource`;
CREATE TABLE IF NOT EXISTS `dimsource` (
  `sourceID` int(11) NOT NULL AUTO_INCREMENT,
  `sourceName` varchar(7) NOT NULL,
  PRIMARY KEY (`sourceID`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `dimsource`
--

INSERT INTO `dimsource` (`sourceID`, `sourceName`) VALUES
(1, 'Web'),
(2, 'Android'),
(3, 'iPhone'),
(4, 'Unknown');

-- --------------------------------------------------------

--
-- Structure de la table `dimtime`
--

DROP TABLE IF EXISTS `dimtime`;
CREATE TABLE IF NOT EXISTS `dimtime` (
  `timeID` int(11) NOT NULL AUTO_INCREMENT,
  `timeAltID` varchar(8) NOT NULL,
  `dayOfWeek` varchar(3) NOT NULL,
  `day` varchar(2) NOT NULL,
  `month` varchar(2) NOT NULL,
  `monthName` varchar(8) NOT NULL,
  `year` varchar(4) NOT NULL,
  `season` varchar(6) NOT NULL,
  PRIMARY KEY (`timeID`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `dimtime`
--

INSERT INTO `dimtime` (`timeID`, `timeAltID`, `dayOfWeek`, `day`, `month`, `monthName`, `year`, `season`) VALUES
(1, '20200505', 'Tue', '05', '05', 'May', '2020', 'spring'),
(2, '20200504', 'Mon', '04', '05', 'May', '2020', 'spring');

-- --------------------------------------------------------

--
-- Structure de la table `factcovcase`
--

DROP TABLE IF EXISTS `factcovcase`;
CREATE TABLE IF NOT EXISTS `factcovcase` (
  `locationID` int(11) NOT NULL,
  `timeID` int(11) NOT NULL,
  `nbrOfCases` int(11) NOT NULL,
  `nbrOfDeath` int(11) NOT NULL,
  `nbrOfRecovered` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `factsentiment`
--

DROP TABLE IF EXISTS `factsentiment`;
CREATE TABLE IF NOT EXISTS `factsentiment` (
  `conceptID` int(11) NOT NULL,
  `locationID` int(11) NOT NULL,
  `languageID` int(11) NOT NULL,
  `timeID` int(11) NOT NULL,
  `averageSentiment` float NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `factsentiment`
--

INSERT INTO `factsentiment` (`conceptID`, `locationID`, `languageID`, `timeID`, `averageSentiment`) VALUES
(1, 1, 1, 1, 0),
(1, 5, 2, 2, 0.25),
(1, 3, 2, 2, 0),
(1, 4, 2, 2, 0.25),
(1, 1, 2, 2, 0.194444),
(1, 5, 2, 1, 0.375),
(1, 1, 2, 1, 0.219643),
(1, 7, 3, 1, 0),
(1, 8, 3, 1, 0),
(1, 1, 3, 1, 0),
(2, 10, 2, 2, 0.585938),
(2, 11, 2, 2, 0.585938),
(2, 9, 2, 2, 0.135417),
(2, 15, 2, 2, 0),
(2, 13, 2, 1, 0.0520833),
(2, 12, 2, 1, 0.25),
(2, 16, 4, 1, 0),
(2, 1, 5, 2, 0),
(2, 17, 6, 2, 0),
(2, 18, 3, 2, 0.113636),
(2, 1, 3, 1, -0.09375);

-- --------------------------------------------------------

--
-- Structure de la table `facttweet`
--

DROP TABLE IF EXISTS `facttweet`;
CREATE TABLE IF NOT EXISTS `facttweet` (
  `conceptID` int(11) NOT NULL,
  `locationID` int(11) NOT NULL,
  `sourceID` int(11) NOT NULL,
  `languageID` int(11) NOT NULL,
  `timeID` int(11) NOT NULL,
  `sentimentID` int(11) NOT NULL,
  `numberOfTweets` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `facttweet`
--

INSERT INTO `facttweet` (`conceptID`, `locationID`, `sourceID`, `languageID`, `timeID`, `sentimentID`, `numberOfTweets`) VALUES
(1, 1, 1, 1, 1, 1, 1),
(1, 2, 2, 2, 2, 2, 1),
(1, 1, 2, 2, 1, 1, 2),
(1, 1, 2, 2, 1, 2, 1),
(1, 3, 3, 2, 2, 1, 1),
(1, 1, 3, 2, 2, 1, 2),
(1, 4, 3, 2, 2, 2, 1),
(1, 2, 3, 2, 2, 2, 1),
(1, 1, 3, 2, 1, 1, 1),
(1, 1, 3, 2, 1, 2, 1),
(1, 5, 4, 2, 2, 2, 1),
(1, 5, 4, 2, 1, 2, 2),
(1, 6, 4, 2, 1, 2, 1),
(1, 1, 1, 2, 2, 2, 5),
(1, 7, 2, 3, 1, 1, 1),
(1, 1, 2, 3, 1, 1, 1),
(1, 8, 3, 3, 1, 1, 1),
(2, 9, 2, 2, 2, 1, 2),
(2, 10, 2, 2, 2, 2, 1),
(2, 11, 2, 2, 2, 2, 1),
(2, 1, 2, 2, 2, 2, 1),
(2, 12, 2, 2, 1, 1, 1),
(2, 1, 3, 2, 2, 1, 1),
(2, 9, 3, 2, 2, 2, 1),
(2, 13, 3, 2, 1, 2, 1),
(2, 14, 1, 2, 2, 3, 1),
(2, 15, 1, 2, 2, 1, 1),
(2, 1, 1, 2, 1, 2, 1),
(2, 16, 3, 4, 1, 1, 1),
(2, 1, 1, 5, 2, 1, 1),
(2, 17, 3, 6, 2, 1, 1),
(2, 18, 2, 3, 2, 2, 1),
(2, 1, 2, 3, 1, 3, 1),
(2, 1, 2, 3, 1, 1, 6),
(2, 1, 3, 3, 1, 1, 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
