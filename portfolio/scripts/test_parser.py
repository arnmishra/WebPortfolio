import unittest

from parser import parse_files


class TestGraph(unittest.TestCase):

    def test_create_projects(self):
        """ Test that the shopping project is correctly created with relevant metadata. """
        projects = parse_files(svn_list="portfolio/data/test_svn_list.xml", svn_log="portfolio/data/test_svn_log.xml")
        self.assertTrue("shopping" in projects)
        self.assertTrue("list1.txt" in projects["shopping"])
        self.assertTrue("list2.txt" in projects["shopping"])
        self.assertEqual(projects["shopping"]["date"], "08/28/2016 05:57:16 PM")
        self.assertEqual(projects["shopping"]["version"], "1073")
        self.assertEqual(projects["shopping"]["summary"], "Moved grocery to shopping for clarity")

    def test_create_files(self):
        """ Test that the list1.txt file is correctly created in the shopping directory. """
        projects = parse_files(svn_list="portfolio/data/test_svn_list.xml", svn_log="portfolio/data/test_svn_log.xml")
        self.assertEqual(projects["shopping"]["list1.txt"]["size"], "56")
        self.assertEqual(projects["shopping"]["list1.txt"]["type"], "Text File")
        self.assertEqual(projects["shopping"]["list1.txt"]["path"], "/agmishr2/shopping/list1.txt")
        self.assertEqual(projects["shopping"]["list1.txt"]["version"], "1073")
        self.assertEqual(projects["shopping"]["list1.txt"]["author"], "agmishr2")
        self.assertEqual(projects["shopping"]["list1.txt"]["summary"], "Moved grocery to shopping for clarity")
        self.assertEqual(projects["shopping"]["list1.txt"]["date"], "08/28/2016 05:57:16 PM")
        expected_url = "https://subversion.ews.illinois.edu/svn/fa16-cs242/agmishr2/shopping/list1.txt"
        self.assertEqual(projects["shopping"]["list1.txt"]["url"], expected_url)

    def test_modified_files(self):
        """ Test that list2's summary isn't 'Add List 2' and that its version isn't '1065' after modification. """
        projects = parse_files(svn_list="portfolio/data/test_svn_list.xml", svn_log="portfolio/data/test_svn_log.xml")
        self.assertEqual(projects["shopping"]["list2.txt"]["summary"], "Moved grocery to shopping for clarity")
        self.assertEqual(projects["shopping"]["list2.txt"]["version"], "1073")

    def test_delete_directory(self):
        """ Test that the grocery directory is deleted from the final projects dictionary. """
        projects = parse_files(svn_list="portfolio/data/test_svn_list.xml", svn_log="portfolio/data/test_svn_log.xml")
        self.assertTrue("grocery" not in projects)

    def test_delete_file(self):
        """ Test that the list3.txt file is deleted from the final shopping dictionary. """
        projects = parse_files(svn_list="portfolio/data/test_svn_list.xml", svn_log="portfolio/data/test_svn_log.xml")
        self.assertTrue("list3.txt" not in projects["shopping"])


if __name__ == '__main__':
    unittest.main()
