def register_worker_commands(cli):
    @cli.command()
    def worker():
        from prefect import deploy
        from prefect import flow, serve
        from mtmai.flows.flow_site import flow_cms_site
        from mtmai.flows.article_gen import flow_article_gen

        deploy_flow_article_gen = flow_article_gen.to_deployment(name="flow_article_gen")
        deploy_flow_cms_site = flow_cms_site.to_deployment(name="flow_cms_site")
        serve(deploy_flow_article_gen, deploy_flow_cms_site)
        # deploy(
        #   # Use the `to_deployment` method to specify configuration
        #   #specific to each deployment
        #   flow_article_gen.to_deployment("my-deployment-1"),
        #   # my_flow_2.to_deployment("my-deployment-2"),

        #   # Specify shared configuration for both deployments
        #   image="my-docker-image:dev",
        #   push=False,
        #   work_pool_name="my-work-pool",
        # )

        print("启动 worker")
