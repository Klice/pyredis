class RedisCommand:
    def __init__(self, name, main_params=None, all_args=None, param_types=None, allow_extra=False):
        self.name = name
        if main_params is None:
            self.main_params = []
        else:
            self.main_params = main_params
        if all_args is None:
            self.all_args = []
        else:
            self.all_args = all_args
        if param_types is None:
            self.param_types = {}
        else:
            self.param_types = param_types
        self.allow_extra = allow_extra
        self.flags, self.params = self._get_flags_and_extra_params()

    def _get_flags_and_extra_params(self):
        flags = {}
        params = {}
        all_args_flatten = {}
        for i in self.all_args:
            if type(i) is list:
                for m in i:
                    all_args_flatten[m] = i
            else:
                all_args_flatten[i] = []
        for a in all_args_flatten:
            if a in self.param_types:
                params[a] = all_args_flatten[a]
            else:
                flags[a] = all_args_flatten[a]
        return flags, params

    def _check_mutually_exclusive(self, arg, res):
        if arg in self.params:
            exclusive_list = self.params[arg]
        elif arg in self.flags:
            exclusive_list = self.flags[arg]
        else:
            return True
        for m in exclusive_list:
            if m in self.flags:
                if f"is_{m.lower()}" in res:
                    raise Exception(f"{self.params[arg]} are mutually exclusive")
            if m in self.params:
                if m.lower() in res:
                    raise Exception(f"{self.params[arg]} are mutually exclusive")

    def _check_valid_arg(self, a):
        if not self.allow_extra and (a not in self.flags and a not in self.params):
            raise Exception(f"Invalid argument: {a}")

    def parse(self, args):
        args_iter = iter(args)
        res = {}
        for p in self.main_params:
            res[p] = next(args_iter)

        for a in args_iter:
            self._check_valid_arg(a)
            self._check_mutually_exclusive(a, res)
            if a in self.flags:
                res[f"is_{a.lower()}"] = True
            if a in self.params:
                v = next(args_iter)
                if type(v) is not self.param_types[a]:
                    raise Exception(f"Paramter {a} value should be type {self.param_types[a]}")
                res[a.lower()] = v
        return res
