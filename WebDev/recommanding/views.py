from django.shortcuts import render
from django.views.generic import View
# Create your views here.
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"


class RecommendingView(View):

    TEMPLATE = 'recommending.html'
    driver = GraphDatabase.driver(uri, auth=("yexiao", "yexiao"))

    @staticmethod
    def _get_movie_of(tx, name):
        """

        :param tx:
        :param name:
        :return:
        """
        movies = []
        result = tx.run("MATCH (a:Person)-[:ACTED_IN]->(f) "
                        "WHERE a.name = $name "
                        "RETURN f.title AS movie", name=name)
        for movie in result:
            movies.append(movie)
        return movies


    @staticmethod
    def _get_frist_25(tx):
        """

        :param tx:
        :return:
        """
        result = []
        r = tx.run("MATCH (n:Movie) RETURN n.tagline AS tagline, n.title AS title, n.released as rel LIMIT 25")
        for record in r:
            temp = {'tagline': record['tagline'], 'title': record['title'], 'release date': record['rel']}
            result.append(temp)
        return result

    def get(self, request):
        # to do, add music, add table
        with self.driver.session() as session:
            data = session.read_transaction(self._get_frist_25)

        return render(request, self.TEMPLATE, {'data': data})