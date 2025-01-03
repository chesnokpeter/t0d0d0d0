



# class UnitOfWork():
#     def __init__(self, repos: list[AbsRepo], connectors: list[AbsConnector]):
#         self.connectors = connectors
#         self.repo_names = [repo.reponame for repo in repos]
#         [setattr(self, repo.reponame, repo) for repo in repos]
#         for r in repos:
#             if r.require_connector not in {c.connector_name for c in connectors}:
#                 raise NoConnectorForRepo(f'No Connector For Repo "{r.reponame}"')

#     async def __aenter__(self):
#         for c in self.connectors:
#             await c.connect()
#             for repo_name in self.repo_names:
#                 repo: AbsRepo = getattr(self, repo_name)
#                 if repo.require_connector == c.connector_name:
#                     repo(c.session)

#         return self

#     async def __aexit__(self, *args):
#         await gather(*(c.close() for c in self.connectors))

#     async def commit(self):
#         await gather(*(c.commit() for c in self.connectors))

#     async def rollback(self):
#         await gather(*(c.rollback() for c in self.connectors))
