from django.shortcuts import render
from django.views.generic import View
# Create your views here.
from neo4j import GraphDatabase
from WebDev.settings import driver


class RecommendingView(View):

    TEMPLATE = 'recommending.html'

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
        r = tx.run("MATCH (n:Music) RETURN n.hasKeyword AS keyword, n.id AS id, n.hasTag as tag LIMIT 25")
        for record in r:
            temp = {'tagline': record['tag'], 'keyword': record['keyword'], 'id': record['id']}
            result.append(temp)
        return result

    def get(self, request):
        # to do, add music, add table
        with driver.session() as session:
            data = session.read_transaction(self._get_frist_25)

        return render(request, self.TEMPLATE, {'data': data})